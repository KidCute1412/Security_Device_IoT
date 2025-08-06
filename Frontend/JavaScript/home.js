let reedSensorValue = false; // Simulated initial state
let pirSensorValue = false; // Simulated initial state
let vibrationSensorValue = false; // Simulated initial state






function getAndUpdateStatus(){
  // From API
  fetch("http://localhost:5000/api/get_all_status")
    .then(response => response.json())
    .then(data => {
      if (data.status === "OKE") {
      

         // Update PIR Sensor
        if (data.pir_status) {
          window.pir_status = data.pir_status;
          updatePirSensor(window.pir_status);
        }

        // Update Vibration Sensor
        if (data.vibration_status) {
          window.vibration_status = data.vibration_status;
          updateVibrationSensor(window.vibration_status);
        }

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


// PIR SENSOR
function updatePirSensor(isMotionDetected) {
  const img = document.getElementById("pir-status-icon");
  const text = document.getElementById("pir-text");

  if (isMotionDetected) {
    img.src = "assets/yes_motion.png";
    text.textContent = "🚨 Phát hiện chuyển động";
  } else {
    img.src = "assets/no_motion.png";
    text.textContent = "✅ Không có chuyển động";
  }
}


// VIBRATION SENSOR
function updateVibrationSensor(isVibrationDetected) {
  const img = document.getElementById("vibration-status-icon");
  const text = document.getElementById("vibration-text");

  if (isVibrationDetected) {
    img.src = "assets/yes_vibration.png";
    text.textContent = "⚠️ Phát hiện rung động";
  } else {
    img.src = "assets/no_vibration.png";
    text.textContent = "✅ Không có rung động";
  }
}


function initHomePage() {
  updatePirSensor(window.pir_status);
  updateVibrationSensor(window.vibration_status);
}