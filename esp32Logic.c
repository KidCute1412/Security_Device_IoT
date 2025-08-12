#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <Preferences.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcdDisplay(0x27, 16, 2);
const int vibrationPin = 22;
const int pirPin = 14;
const int ledPin[4] = {21, 19, 35, 33};
const int buzzerPin = 18;
int pir = 0;
int vibration = 0;
int led = 1;
int buzzer = 1;
int lcd = 0;
int lastLcdStatus = -1;

bool lastVibrationState = HIGH;

unsigned long lastSendTime = 0;
unsigned long ledStartTime = 0;
bool ledOn = false;

String controlTopic = "";
String sensorTopic = "";

//***Set server***
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
const char* mqttServer = "broker.hivemq.com"; 
int port = 1883;
String username ="";


const int DNS_PORT = 53;
WebServer server(80);
DNSServer dnsServer;
Preferences prefs;
String ssid, password;
bool apActive = false;
unsigned long connectStartTime = 0;
bool tryingToConnect = false;
bool notifyWebClient = false;
unsigned long notifyStartTime = 0;
const unsigned long CONNECT_TIMEOUT = 10000; // 10 giây
const unsigned long NOTIFY_DURATION = 5000;  // 5 giây giữ trang Connected
unsigned long lastReconnectAttempt = 0;
const unsigned long RECONNECT_INTERVAL = 5000; // 5 giây

IPAddress apIP(192, 168, 4, 1);
IPAddress netMsk(255, 255, 255, 0);

//==============PushSafer================
const char* host = "www.pushsafer.com"; // Không cần https:// khi dùng port 80
const int httpPort = 80;
const char* request = "/api?k=CCnyZqhQ1nV83bfWiZfx&m=Warning%3A%20a%20strange%20person%20is%20trying%20to%20break%20into%20your%20house";
// Thời gian chặn gửi lại (5 phút)
const unsigned long SEND_WARNING_INTERVAL = 300000; // 5 phút
unsigned long lastSendWarningTime = 0;
bool firstSend = true;

// ===== Captive portal: redirect tất cả truy vấn DNS về ESP32 =====
void startDNSServer() {
  dnsServer.start(DNS_PORT, "*", apIP);
  Serial.println("DNS server started for captive portal");
}

// ===== Giao diện chính =====
void handleRoot() {
  String html = "<html><body>"
                "<h2>WiFi Config</h2>"
                "<form action='/connect' method='POST'>"
                "SSID: <input type='text' name='ssid'><br>"
                "Password: <input type='password' name='pass'><br>"
                "<input type='submit' value='Connect'>"
                "</form></body></html>";
  server.send(200, "text/html", html);
}

// ===== Xử lý khi nhấn Connect =====
void handleConnectAndStatus() {
  if (server.method() == HTTP_POST) {
    // Xử lý POST: lấy dữ liệu ssid, pass rồi bắt đầu kết nối
    ssid = server.arg("ssid");
    password = server.arg("pass");

    WiFi.disconnect(true, false);
    delay(100);

    WiFi.mode(WIFI_AP_STA);
    WiFi.begin(ssid.c_str(), password.c_str());

    connectStartTime = millis();
    tryingToConnect = true;

    Serial.println("Trying to connect to WiFi: " + ssid);

    // Gửi trang báo đang kết nối, tự refresh sau 2s sang trang trạng thái
    server.send(200, "text/html",
                "<h3>Connecting...</h3>"
                "<meta http-equiv='refresh' content='2;url=/connect'>");
  } else {
    // Xử lý GET: trả về trang trạng thái kết nối
    if (WiFi.status() == WL_CONNECTED) {
      String html = "<html><body>"
                    "<h2>Connected!</h2>"
                    "<p>IP: " + WiFi.localIP().toString() + "</p>"
                    "<p>You can close this page.</p>"
                    "</body></html>";
      server.send(200, "text/html", html);

      if (!notifyWebClient) {
        notifyWebClient = true;
        notifyStartTime = millis();
      }
    } else {
      if (!tryingToConnect) {
        String html = "<html><body>"
                      "<h2>Failed to connect!</h2>"
                      "<p>Could not connect to WiFi network.</p>"
                      "<p><a href='/'>Try again</a></p>"
                      "</body></html>";
        server.send(200, "text/html", html);
      } else {
        server.send(200, "text/html",
                    "<h3>Still connecting...</h3>"
                    "<meta http-equiv='refresh' content='2;url=/connect'>");
      }
    }
  }
}


// ===== Redirect mọi HTTP request về trang config (captive portal) =====
void handleCaptivePortal() {
  Serial.println("Captive portal request intercepted");

  String html = "<html><body>"
                "<h2>ESP32 WiFi Setup</h2>"
                "<form action='/connect' method='POST'>"
                "SSID: <input type='text' name='ssid'><br>"
                "Password: <input type='password' name='pass'><br>"
                "<input type='submit' value='Connect'>"
                "</form></body></html>";

  server.send(200, "text/html", html);
}


// ===== AP Mode =====
void startAPMode() {
  WiFi.disconnect(true, true);
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(apIP, apIP, netMsk);
  WiFi.softAP("ESP32_Setup", "12345678");

  Serial.println("AP Mode: Connect to ESP32_Setup, pass: 12345678");

  startDNSServer();

  server.on("/", handleRoot);
  server.on("/connect", HTTP_ANY, handleConnectAndStatus);

  // Redirect mọi request khác về trang config
  server.onNotFound(handleCaptivePortal);

  server.begin();

  apActive = true;
  tryingToConnect = false;
}

// ===== Kết nối lại WiFi cũ =====
void connectToSavedWiFi() {
  prefs.begin("wifi", true); // read-only
  String savedSSID = prefs.getString("ssid", "");
  String savedPASS = prefs.getString("pass", "");
  prefs.end();

  if (savedSSID != "") {
    Serial.println("Trying saved WiFi: " + savedSSID);
    WiFi.mode(WIFI_STA);
    WiFi.begin(savedSSID.c_str(), savedPASS.c_str());
    connectStartTime = millis();
    tryingToConnect = true;
  } else {
    Serial.println("No saved WiFi. Starting AP mode...");
    startAPMode();
  }
}

// ===== Lưu WiFi =====
void saveWiFiCredentials(const String& ssid, const String& pass) {
  prefs.begin("wifi", false);
  prefs.putString("ssid", ssid);
  prefs.putString("pass", pass);
  prefs.end();
  Serial.println("WiFi credentials saved.");
}

// ===== Check trạng thái WiFi =====
void checkWiFiStatus() {
  dnsServer.processNextRequest();

  if (WiFi.status() == WL_CONNECTED && (apActive || tryingToConnect)) {
    Serial.println("Wi-Fi connected! IP: " + WiFi.localIP().toString());

    saveWiFiCredentials(WiFi.SSID(), password);
    tryingToConnect = false;
  }

  if (notifyWebClient && millis() - notifyStartTime > NOTIFY_DURATION) {
    if (apActive) {
      Serial.println("Turning off AP...");
      WiFi.softAPdisconnect(true);
      WiFi.mode(WIFI_STA);
      apActive = false;
    }
    notifyWebClient = false;
  }

  if (tryingToConnect && millis() - connectStartTime > CONNECT_TIMEOUT) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("Failed to connect.");
      if (!apActive) startAPMode();
      tryingToConnect = false;
    }
  }

  if (!apActive && WiFi.status() != WL_CONNECTED) {
    if (millis() - lastReconnectAttempt > RECONNECT_INTERVAL) {
      Serial.println("Lost Wi-Fi connection. Returning to AP mode...");
      startAPMode();
      lastReconnectAttempt = millis();
    }
  }
}

void mqttConnect() {
  while(!mqttClient.connected()) {
    Serial.println("Attemping MQTT connection...");
    String clientId = "ESP32Client-" + String(random(0xffff), HEX);
    if(mqttClient.connect(clientId.c_str())) {
      Serial.println("connected");

      //***Subscribe all topic you need***
      mqttClient.subscribe("/23127061_23127158_23127404/unification");
      
    }
    else {
      Serial.print(mqttClient.state());
      Serial.println("try again in 5 seconds");
      delay(5000);
    }
  }
}

//MQTT Receiver
void callback(char* topic, byte* message, unsigned int length) {
  Serial.println(topic);
  String msg;
  for(int i=0; i<length; i++) {
    msg += (char)message[i];
  }
  Serial.println(msg);

  if (String(topic) == "/23127061_23127158_23127404/unification") {

    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, msg);
    if (error) {
      Serial.print("JSON error: ");
      Serial.println(error.c_str());
      return;
    }

    username = doc["username"].as<String>();
    controlTopic = "/23127061_23127158_23127404/" + username + "/control_data";
    mqttClient.subscribe(controlTopic.c_str());
    Serial.print("Subscribed to: ");
    Serial.println(controlTopic);
    sensorTopic = "/23127061_23127158_23127404/" + username + "/received_data";

    // Tạo JSON để gửi lại
    StaticJsonDocument<200> responseDoc;
    responseDoc["pir_sensor"] = pir;
    responseDoc["vibration_sensor"] = vibration;
    responseDoc["led"] = led;
    responseDoc["buzzer"]  = buzzer;
    responseDoc["lcd"] = lcd;

    char buffer[256];
    size_t len = serializeJson(responseDoc, buffer);

    // Gửi JSON qua topic động
    mqttClient.publish(sensorTopic.c_str(), buffer, len);
    Serial.print("Published JSON to ");
    Serial.println(sensorTopic);
    Serial.println(buffer);
  }

  if (String(topic) == controlTopic.c_str()) 
 {
  StaticJsonDocument<256> controlDoc;
  DeserializationError controlErr = deserializeJson(controlDoc, msg);
  if (controlErr) {
    Serial.print("Control JSON error: ");
    Serial.println(controlErr.c_str());
    return;
  }

  led = controlDoc["commands"]["led_status"];
  buzzer = controlDoc["commands"]["buzzer_status"];
  lcd = controlDoc["commands"]["lcd_status"];
  // Sau này bạn có thể dùng để điều khiển chân GPIO

  Serial.println("Received control data:");
  Serial.print("LED: "); Serial.println(led);
  Serial.print("Buzzer: "); Serial.println(buzzer);
  Serial.print("LCD: "); Serial.println(lcd);
  }
}

void handleSensorData() {
  unsigned long now = millis();

  // Đọc cảm biến rung liên tục
  bool currentVibration = digitalRead(vibrationPin);

  // Phát hiện cạnh xuống (xung rung rất ngắn)
  if (lastVibrationState == HIGH && currentVibration == LOW) {
    vibration  = 1;
  }
  lastVibrationState = currentVibration;

  if (lcd != lastLcdStatus || lcd == 1 && (led == 1 || buzzer == 1)) {
  StaticJsonDocument<200> sendModeData;
  if (lcd == 0) {
      led = 1;
      buzzer = 1;
      sendModeData["led"] = led;
      sendModeData["buzzer"] = buzzer;
      sendModeData["lcd"] = 0;
    } else {
      led = 0;
      buzzer = 0;
      sendModeData["pir_sensor"] = 0;
      sendModeData["vibration_sensor"] = 0;
      sendModeData["led"] = led;
      sendModeData["buzzer"] = buzzer;
      sendModeData["lcd"] = 1;
    }
    char buffer1[256];
    size_t len = serializeJson(sendModeData, buffer1);

    if (sensorTopic != "") {
      mqttClient.publish(sensorTopic.c_str(), buffer1, len);
    }
  }

  

  // Gửi trạng thái cảm biến lên mỗi 1 giây
  if (now - lastSendTime >= 1000) {
    pir = digitalRead(pirPin);
    
    Serial.print("Status - PIR: ");
    Serial.print(pir);
    //Serial.print(" | Vibration: ");
    //Serial.println(vibration ? "Detected" : "No");
    
    // Gửi MQTT ở đây nếu có:
    // mqttClient.publish("topic", "{...}");
    // Tạo JSON để gửi lại
    
    StaticJsonDocument<200> sendData;
    if (lcd == 0) {
      sendData["pir_sensor"] = pir;
      sendData["vibration_sensor"] = vibration;
    }
    
    char buffer2[256];
    size_t len = serializeJson(sendData, buffer2);

    // Gửi JSON qua topic động
    if (sensorTopic != "") {
      mqttClient.publish(sensorTopic.c_str(), buffer2, len);
    }
    
    //Serial.print("Published JSON to ");
    //Serial.println(sensorTopic);
    Serial.println(buffer2);
    if (vibration == 1 && pir == 1 && lcd == 0) {
      if ((WiFi.status() == WL_CONNECTED) && ((now - lastSendWarningTime >= SEND_WARNING_INTERVAL) || firstSend)) {
        Serial.println("Gửi thông báo...");
        //sendRequest();
        lastSendWarningTime = now; // Cập nhật thời gian gửi
        firstSend = false;
      }
      triggerAlarm();
    }
    vibration = 0; // reset sau khi báo
    lastSendTime = now;

    
  }

  
}

void triggerAlarm() {
  Serial.println("ALARM TRIGGERED!");

  if(buzzer == 1) tone(buzzerPin, 1000); // Phát âm thanh cố định
  unsigned long startTime = millis();
  bool ledState = false;
  unsigned long lastBlinkTime = 0;

  while (millis() - startTime < 5000) {
    // LED nhấp nháy mỗi 200ms
    if (led == 1) {
      if (millis() - lastBlinkTime >= 200) {
      lastBlinkTime = millis();
      ledState = !ledState;
      for(int i = 0; i < 4; i++) {
        digitalWrite(ledPin[i], ledState);
      }
      }
    }
    
  }

  // Tắt còi và LED
  noTone(buzzerPin);
  for(int i = 0; i < 4; i++) 
  {
    digitalWrite(ledPin[i], LOW);
  }
}

void lcdShowStatus(int lcd) {
  if (lcd != lastLcdStatus) {    // chỉ khi trạng thái thay đổi mới update LCD
    lcdDisplay.clear();
    lcdDisplay.setCursor(0, 0);
    if (lcd == 0) {
      lcdDisplay.print("Armed Mode");
    } else if (lcd == 1) {
      lcdDisplay.print("Home Mode");
    }
    lastLcdStatus = lcd;          // cập nhật lại trạng thái mới
  }
}

//============PushSafer===============
void sendRequest() {
  WiFiClient client;
  while(!client.connect(host, httpPort)) {
    Serial.println("connection fail");
    delay(1000);
  }
  client.print(String("GET ") + request + " HTTP/1.1\r\n"
              + "Host: " + host + "\r\n"
              + "Connection: close\r\n\r\n");
  delay(500);

  while(client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
}

void setup() {
  Serial.begin(115200);
  //connectToSavedWiFi();
  Serial.print("Connecting to WiFi");

  pinMode(vibrationPin, INPUT);
  pinMode(pirPin, INPUT);
  for (int i = 0; i < 4; i++) {
    pinMode(ledPin[i], OUTPUT);  
  }
  pinMode(buzzerPin, OUTPUT);
  Wire.begin(25, 26);
  lcdDisplay.init();
  lcdDisplay.backlight();
  lcdDisplay.print("Xin chao");

  mqttClient.setServer(mqttServer, port);
  mqttClient.setCallback(callback);
  mqttClient.setKeepAlive( 90 );
}

void loop() {
  dnsServer.processNextRequest();
  server.handleClient();
  checkWiFiStatus();

  if (WiFi.status() == WL_CONNECTED) {
  if (!mqttClient.connected()) {
    mqttConnect();
  }
  mqttClient.loop();
  
  } else {
    // WiFi chưa kết nối, có thể chờ hoặc xử lý kết nối WiFi
    Serial.println("Waiting for WiFi connection...");
  }
  handleSensorData();
  lcdShowStatus(lcd);

  
  // xử lý dữ liệu của cảm biến
  
}
