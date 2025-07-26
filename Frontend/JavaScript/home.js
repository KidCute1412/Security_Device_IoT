// REED SENSOR
function updateReedSensor(isOpen) {
  const img = document.getElementById("reed-status-icon");
  const text = document.getElementById("reed-text");

  if (isOpen) {
    img.src = "assets/open_lock.png";
    text.textContent = "🔓 Cửa đang mở";
  } else {
    img.src = "assets/close_lock.png";
    text.textContent = "🔒 Cửa đang đóng";
  }
}

let reedSensorValue = false; // Simulated initial state
setInterval(() => {
  reedSensorValue = !reedSensorValue; // Toggle state for simulation
  updateReedSensor(reedSensorValue);
}, 5000); // Update every 5 seconds

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
let pirSensorValue = false; // Simulated initial state
setInterval(() => {
  pirSensorValue = !pirSensorValue; // Toggle state for simulation
  updatePirSensor(pirSensorValue);
}, 5000); // Update every 5 seconds

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
let vibrationSensorValue = false; // Simulated initial state
setInterval(() => {
  vibrationSensorValue = !vibrationSensorValue; // Toggle state for simulation
  updateVibrationSensor(vibrationSensorValue);
}
, 5000); // Update every 5 seconds




