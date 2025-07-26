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




// INIT DATA PAGE
function initDataPage() {
    loadTimesChart();
    loadTrendChart();

}
