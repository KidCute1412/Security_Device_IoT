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
        window.led_status = 1; // Update global variable
    }
    else {
        ledStatus.textContent = "OFF";
        ledStatus.style.color = "black";
        checkboxElement.checked = false; // Update checkbox state
        window.led_status = 0; // Update global variable
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
        window.buzzer_status = 1; // Update global variable
    }
    else {
        buzzerStatus.textContent = "OFF";
        buzzerStatus.style.color = "black";
        checkboxElement.checked = false; // Update checkbox state
        window.buzzer_status = 0; // Update global variable
    }
}




// LCD status
function initLCDStatus(){
    // LOAD FROM ESP32
    const status = "Chống Trộm"; // Simulated initial state
    updateLcdStatus(status);  // Fixed: use updateLcdStatus consistently
}
function updateLcdStatus(value) {  // Fixed: renamed from updateLCDStatus to updateLcdStatus
    const lcdStatus = document.getElementById("lcd-status");
    const lcdSelect = document.getElementById("lcd-select");
  
    if (value === '0') {
        lcdStatus.textContent = "Chống Trộm Mode";
        lcdStatus.style.color = "Red";
        lcdSelect.value = 0; // Update select state
        lcdSelect.style.backgroundColor = "#e96e8f"; // Change select color to match
        window.lcd_status = 0; // Update global variable
    } else if (value === '1') {
        lcdStatus.textContent = "Gia Chủ Mode";
        lcdStatus.style.color = "blue";
        lcdSelect.value = 1; // Update select state
        lcdSelect.style.backgroundColor = "#6e8fe9"; // Change select color to match
        window.lcd_status = 1; // Update global variable
    }
}







function sendCommandToDevices(){
    const data = {
        "led_status": window.led_status,
        "buzzer_status": window.buzzer_status,
        "lcd_status": window.lcd_status
    }
    fetch("http://localhost:5000/api/control_devices", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "OKE") {
            console.log("Command sent successfully");
        } else {
            console.error("Error sending command:", data.message);
        }
    })
}


// INIT SETTING PAGE
function initSettingsPage(){
    updateBuzzerStatus(window.buzzer_status);
    updateLedStatus(window.led_status);
    updateLcdStatus(String(window.lcd_status));
}

setInterval(() => {
    initSettingsPage();
}, 4); 

