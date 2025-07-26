function loadPage(page) {
  fetch(`pages/${page}.html`)
    .then(res => res.text())
    .then(data => {
      document.getElementById("main-content").innerHTML = data;

      window.location.hash = page;
      if (page === 'data') initDataPage();
      if (page === 'home') {
        updateReedSensor(false);
        updatePirSensor(false);
        updateVibrationSensor(false);
      }
      if (page === 'settings') initSettingsPage();
    });
  
}


function logout(){
    window.location.href = "../HTML/login.html";
}

function toggleSidebar() {
  const sidebar = document.getElementById("side-bar");
  sidebar.style.display = (sidebar.style.display === "none") ? "block" : "none";
}

window.onload = function(){
  const page = window.location.hash ? window.location.hash.substring(1) : "home";
  loadPage(page);
}

// HOME page

// function loadDataChart() {
//   const ctx = document.getElementById("times-chart").getContext("2d");
//   new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
//       datasets: [{
//         label: 'Cảnh báo',
//         data: [10, 12, 14, 9, 20, 18, 25],
//         backgroundColor: 'rgba(255, 99, 132, 0.6)',
//         borderColor: 'rgba(255, 99, 132, 1)',
//         borderWidth: 1
//       }]
//     },
//     options: {
//       responsive: true,
//       maintainAspectRatio: false
//     }
//   });
  
// }