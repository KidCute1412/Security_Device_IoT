// TIMES-CHART
var timesChart;
function loadTimesChart(){
    var canvas = document.getElementById("times-chart");
    var context = canvas.getContext("2d");
    timesChart = new Chart(context, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Số lần cảnh báo(trong tuần hiện tại)',
                data: [11, 20, 15, 30, 50, 12, 18],
                backgroundColor: 'rgba(105, 164, 236, 1)'
            }]
        }
        ,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'black',
                        font: {
                            size: 14
                        }
                    },
                    // đơn vị
                    title: {
                        display: true,
                        text: 'Số lần cảnh báo',
                        color: 'DarkBlue',
                        font: {
                            size: 16
                        }
                    }
             
                },
                x: {
                    ticks: {
                        color: 'Blue',
                        font: {
                            size: 14
                        }
                    },
                    title: {
                        display: true,
                        text: 'Ngày trong tuần',
                        color: 'DarkBlue',
                        font: {
                            size: 16
                        }
                    }
                }
            }
        }
    });

}

// Simulated data update function
function getNewTimesData() {
    const newData = Array.from({length: 7}, () => Math.floor(Math.random() * 100));
    return newData;
}   

setInterval(()=>{
    const newData = getNewTimesData();
    timesChart.data.datasets[0].data = newData;
    timesChart.update();
}, 5000); // Update every 5 seconds


// LINE-CHART
var trendChart;
function loadTrendChart() {
    var canvas = document.getElementById("trend-chart");
    var context = canvas.getContext("2d");
    trendChart = new Chart(context, {
        type: 'line',
        data: {
            labels: ['0h', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h',
                 '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h'],
            datasets: [{
                label: 'Xu hướng cảnh báo trong ngày (hôm nay)',
                data: [0, 1, 0, 2, 3, 5, 4, 6, 7, 8, 10, 9, 11,
                 12, 14, 13, 15, 16, 18, 17, 19, 20, 22, 21, 23],
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
                        font: {
                            size: 14
                        }
                    },
                    title: {
                        display: true,
                        text: 'Số lần cảnh báo',
                        color: 'DarkBlue',
                        font: {
                            size: 16
                        }
                    }
                },
                x: {
                    ticks: {
                        color: 'Blue',
                        font: {
                            size: 14
                        }
                    },
                    title: {
                        display: true,
                        text: 'Thời gian trong ngày',
                        color: 'DarkBlue',
                        font: {
                            size: 16
                        }
                    }
                }
            }
        }
    });
}

function getNewTrendData() {
    const newData = Array.from({length: 24}, () => Math.floor(Math.random() * 10));
    return newData;
}
setInterval(() => {
    const newData = getNewTrendData();
    trendChart.data.datasets[0].data = newData;
    trendChart.update();
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
