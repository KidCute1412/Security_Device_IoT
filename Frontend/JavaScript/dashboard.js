function loadPage(page) {
  fetch(`pages/${page}.html`)
    .then(res => res.text())
    .then(data => {
      document.getElementById("main-content").innerHTML = data;

      window.location.hash = page;
      if (page === 'data') initDataPage();
      if (page === 'home') {

        initHomePage();
      }
      if (page === 'settings') initSettingsPage();
    });
  
}


function logout(){
    window.location.href = "../HTML/login.html";
    fetch("http://localhost:5000/api/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (response.ok) {
            console.log("Logout successful");
        } else {
            console.error("Logout failed");
        }
    })
}

function toggleSidebar() {
  const sidebar = document.getElementById("side-bar");
  sidebar.style.display = (sidebar.style.display === "none") ? "block" : "none";
}

window.onload = function(){
  const page = window.location.hash ? window.location.hash.substring(1) : "home";
  loadPage(page);
}


function getAndUpdateStatus(){
  // From API
  fetch("http://localhost:5000/api/get_all_status")
    .then(response => response.json())
    .then(data => {
      if (data.status === "OKE") {
      

        // Update PIR Sensor
        window.pir_status = data.pir_status;
        // Update Vibration Sensor
        window.vibration_status = data.vibration_status;


        window.led_status = data.led_status;
        window.buzzer_status = data.buzzer_status;
        window.lcd_status = data.lcd_status;
      }
      else {
        console.error("Error fetching status:", data.message);
      }
    })
    .catch(error => {
      console.error("Network error:", error);
    });
}



// Initialize status updates with smart timing
function initializeStatusUpdates() {
    console.log("Initializing status updates...");
    
    // Give ESP32 time to respond to unification message before first call
    setTimeout(() => {
        console.log("Making first status call...");
        getAndUpdateStatus();
    }, 2000); // Wait 2 seconds for ESP32 to respond
    
    // Then update every 1 second after the initial delay
    setTimeout(() => {
        console.log("Starting regular interval updates...");
        const intervalId = setInterval(getAndUpdateStatus, 5000);
        window.statusUpdateInterval = intervalId;
    }, 3000); // Start interval after 3 seconds
}

// Function to stop status updates (useful when navigating away)
function stopStatusUpdates() {
    if (window.statusUpdateInterval) {
        clearInterval(window.statusUpdateInterval);
        console.log("Status updates stopped");
    }
}

// Start the updates
initializeStatusUpdates();