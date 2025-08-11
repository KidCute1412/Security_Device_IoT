






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


function updateConclusionText(isMotionDetected, isVibrationDetected) {
  const conclusionText = document.getElementById("conclusion-text");

  if (isMotionDetected && isVibrationDetected) {
    conclusionText.textContent = "Kết luận: Phát hiện đột nhập";
  }
  else if (isMotionDetected && !isVibrationDetected) {
    conclusionText.textContent = "Kết luận: Phát hiện có người";
  }
  else if (!isMotionDetected && isVibrationDetected) {
    conclusionText.textContent = "Kết luận: Phát hiện rung động";
  } else {
    conclusionText.textContent = "Kết luận: Không phát hiện nguy hiểm";
  }
}

function initHomePage() {
  updatePirSensor(window.pir_status);
  updateVibrationSensor(window.vibration_status);
  updateConclusionText(window.pir_status, window.vibration_status);
}

setInterval(() => {
  initHomePage();
}, 1000); // Update every 1 seconds
