// LED status
function initLedStatus(){
    // LOAD FROM ESP32
    const status = true; // Simulated initial state
    updateLedStatus(status);
}
function updateLedStatus(checkbox) {
    const isOn = checkbox;
    const checkboxElement = document.getElementById("checkbox-led");
    const ledStatus = document.getElementById("led-status");
    if (isOn) {
        ledStatus.textContent = "ON";
        ledStatus.style.color = "Red";
        checkboxElement.checked = true; // Update checkbox state
    }
    else {
        ledStatus.textContent = "OFF";
        ledStatus.style.color = "black";
        checkboxElement.checked = false; // Update checkbox state
    }
}

// Relay status
function initRelayStatus(){
    // LOAD FROM ESP32
    const status = true; // Simulated initial state
    updateRelayStatus(status);
}
function updateRelayStatus(checkbox) {
    const isOn = checkbox;
    const checkboxElement = document.getElementById("checkbox-relay");
    const relayStatus = document.getElementById("relay-status");
    if (isOn) {
        relayStatus.textContent = "ON";
        relayStatus.style.color = "Red";
        checkboxElement.checked = true; // Update checkbox state
    }
    else {
        relayStatus.textContent = "OFF";
        relayStatus.style.color = "black";
        checkboxElement.checked = false; // Update checkbox state
    }
}

// Buzzer status
function initBuzzerStatus(){
    // LOAD FROM ESP32
    const status = false; // Simulated initial state
    updateBuzzerStatus(status);
}
function updateBuzzerStatus(checkbox) {
    const isOn = checkbox;
    const checkboxElement = document.getElementById("checkbox-buzzer");
    const buzzerStatus = document.getElementById("buzzer-status");
    if (isOn) {
        buzzerStatus.textContent = "ON";
        buzzerStatus.style.color = "Red";
        checkboxElement.checked = true; // Update checkbox state
    }
    else {
        buzzerStatus.textContent = "OFF";
        buzzerStatus.style.color = "black";
        checkboxElement.checked = false; // Update checkbox state
    }
}










// INIT SETTING PAGE
function initSettingsPage(){
    initLedStatus();
    initRelayStatus();
    initBuzzerStatus();
    // Load other settings if needed   
}

// setInterval(() => {
//     const isLedOn = Math.random() < 0.5; // Simulate LED status change
//     updateLedStatus(isLedOn);
// }, 5000); // Update every 5 seconds