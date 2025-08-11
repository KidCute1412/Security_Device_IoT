// TIMES-CHART
var timesChart;
function loadTimesChart(){
    // Get date range from inputs
    start = document.getElementById("start-date-chart").value;
    end = document.getElementById("end-date-chart").value;
    fetch("http://localhost:5000/api/alerts_per_day")
        .then(response => response.json())
        .then(result => {
            if(result.status === "OKE") {
                var canvas = document.getElementById("times-chart");
                var context = canvas.getContext("2d");
                if (timesChart) timesChart.destroy();
                timesChart = new Chart(context, {
                    type: 'bar',
                    data: {
                        labels: result.labels,
                        datasets: [{
                            label: 'Số lần cảnh báo (theo ngày)',
                            data: result.data,
                            backgroundColor: 'rgba(105, 164, 236, 1)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    color: 'black',
                                    font: { size: 14 }
                                },
                                title: {
                                    display: true,
                                    text: 'Số lần cảnh báo',
                                    color: 'DarkBlue',
                                    font: { size: 16 }
                                }
                            },
                            x: {
                                ticks: {
                                    color: 'Blue',
                                    font: { size: 14 }
                                },
                                title: {
                                    display: true,
                                    text: 'Ngày',
                                    color: 'DarkBlue',
                                    font: { size: 16 }
                                }
                            }
                        }
                    }
                });
            } else {
                alert("Không thể tải dữ liệu cảnh báo: " + result.message);
            }
        })
        .catch(err => {
            alert("Lỗi khi tải dữ liệu cảnh báo: " + err);
        });
}

// Simulated data update function
function getNewTimesData() {
    // Instead of random data, fetch the latest alert data for the current date range
    return fetch("http://localhost:5000/api/alerts_per_day")
        .then(response => response.json())
        .then(result => {
            if (result.status === "OKE") {
                // Update chart labels as well, in case the date range changed
                if (timesChart) {
                    timesChart.data.labels = result.labels;
                }
                return result.data;
            } else {
                return timesChart ? timesChart.data.datasets[0].data : [];
            }
        })
        .catch(() => timesChart ? timesChart.data.datasets[0].data : []);
}

// Replace the setInterval with an async update that fetches real data
setInterval(() => {
    getNewTimesData().then(newData => {
        if (timesChart && newData) {
            timesChart.data.datasets[0].data = newData;
            timesChart.update();
        }
    });
}, 5000);


// LINE-CHART
var trendChart;
function loadTrendChart() {
    fetch("http://localhost:5000/api/alerts_per_hour")
        .then(response => response.json())
        .then(result => {
            if (result.status === "OKE") {
                var canvas = document.getElementById("trend-chart");
                var context = canvas.getContext("2d");
                if (trendChart) trendChart.destroy();
                trendChart = new Chart(context, {
                    type: 'line',
                    data: {
                        labels: result.labels,
                        datasets: [{
                            label: 'Số lần cảnh báo theo giờ (ngày đã chọn)',
                            data: result.data,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.42)',
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    color: 'black',
                                    font: { size: 14 }
                                },
                                title: {
                                    display: true,
                                    text: 'Số lần cảnh báo',
                                    color: 'DarkBlue',
                                    font: { size: 16 }
                                }
                            },
                            x: {
                                ticks: {
                                    color: 'Blue',
                                    font: { size: 14 }
                                },
                                title: {
                                    display: true,
                                    text: 'Giờ trong ngày',
                                    color: 'DarkBlue',
                                    font: { size: 16 }
                                }
                            }
                        }
                    }
                });
            } else {
                alert("Không thể tải dữ liệu cảnh báo theo giờ: " + result.message);
            }
        })
        .catch(err => {
            alert("Lỗi khi tải dữ liệu cảnh báo theo giờ: " + err);
        });
}

function getNewTrendData() {
    return fetch("http://localhost:5000/api/alerts_per_hour")
        .then(response => response.json())
        .then(result => {
            if (result.status === "OKE") {
                if (trendChart) {
                    trendChart.data.labels = result.labels;
                }
                return result.data;
            } else {
                return trendChart ? trendChart.data.datasets[0].data : [];
            }
        })
        .catch(() => trendChart ? trendChart.data.datasets[0].data : []);
}

// Replace the setInterval with an async update that fetches real data
setInterval(() => {
    getNewTrendData().then(newData => {
        if (trendChart && newData) {
            trendChart.data.datasets[0].data = newData;
            trendChart.update();
        }
    });
}, 5000); // Update every 5 seconds

// DATE FILTER

// Today's date
const today = new Date().toISOString().split('T')[0];
function setupDefaultDate(){
    // For chart 1, end date is today, start day is 7 days ago
    const endDate = today;
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 7);
    const formattedStartDate = startDate.toISOString().split('T')[0];
    document.getElementById("start-date-chart").value = formattedStartDate;
    document.getElementById("end-date-chart").value = endDate;
    // For chart 2, only today
    document.getElementById("date-chart").value = today;
}

// Update chart 1 with selected date range
function updateChart1() {
    const start = document.getElementById("start-date-chart").value;
    const end = document.getElementById("end-date-chart").value;
    if (!start || !end) {
        alert("Vui lòng chọn ngày bắt đầu và kết thúc.");
        return;
    }
    const startDate = new Date(start);
    const endDate = new Date(end);
    const diffTime = endDate - startDate;
    if (diffTime < 0) {
        alert("Ngày kết thúc không được trước ngày bắt đầu.");
        return;
    }
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays > 7) {
        alert("Khoảng thời gian không được vượt quá 7 ngày.");
        return;
    }
    // Fetch data to server
    fetch("http://localhost:5000/api/get_date_chart1", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            start_date: start,
            end_date: end
        })
    }).then(response => {
        return response.json();
    }
    ).then(data => {
        if (data.status === "OKE") {
            console.log("Data for chart 1 updated successfully.");
        }
        else {
            alert("Lỗi khi cập nhật dữ liệu biểu đồ 1: " + data.message);
        }
    });
}

// Update chart 2 with selected date
function updateChart2() {
    const date = document.getElementById("date-chart").value;
    if (!date) {
        alert("Vui lòng chọn ngày.");
        return;
    }
    const selectedDate = new Date(date);
    const todayDate = new Date();
    if (selectedDate > todayDate) {
        alert("Ngày chọn không được sau ngày hôm nay.");
        return;
    }
    // Fetch data to server
    fetch("http://localhost:5000/api/get_date_chart2", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            date: date
        })
    }).then(response => {
        return response.json();
    }
    ).then(data => {
        if (data.status === "OKE") {
            console.log("Data for chart 2 updated successfully.");
        }
        else {
            alert("Lỗi khi cập nhật dữ liệu biểu đồ 2: " + data.message);
        }
    });
}

// AI simulated responsive
function aiResponseChart1(){
    // GET data chart 1
    var labels = timesChart.data.labels;
    var data = timesChart.data.datasets[0].data;

    fetch("/api/generative_ai_response/chart1", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
        ,
        body: JSON.stringify({
            labels: labels,
            data: data
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("genai-text-chart1").innerText = data.analysis;
    })
    .catch(error => {
        console.error("Error fetching AI response for chart 1:", error);
        document.getElementById("genai-text-chart1").innerText = "Có lỗi xảy ra khi lấy phản hồi AI.";
    });

}
function aiResponseChart2(){
    // GET data chart 2
    var labels = trendChart.data.labels;
    var data = trendChart.data.datasets[0].data;
    fetch("/api/generative_ai_response/chart2", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
        ,
        body: JSON.stringify({
            labels: labels,
            data: data
        })

    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("genai-text-chart2").innerText = data.analysis;
    })
    .catch(error => {
        console.error("Error fetching AI response for chart 2:", error);
        document.getElementById("genai-text-chart2").innerText = "Có lỗi xảy ra khi lấy phản hồi AI.";
    });
}


// INIT DATA PAGE
function initDataPage() {
    loadTimesChart();
    loadTrendChart();
    setupDefaultDate();
}









// AI responsive
