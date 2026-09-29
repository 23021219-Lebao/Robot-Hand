/*
  Test Code cho Cảm biến lực FSR 402 trên ESP32
  - Cấu hình: Chia áp (Voltage Divider) với điện trở pull-down 10kΩ.
  - Chân tín hiệu: Nối vào chân Analog ADC của ESP32 (Ví dụ: GPIO 34).
*/

const int fsrPin = 34; // Chân đọc Analog (ADC1_CH6 trên ESP32)
int fsrReading = 0;    // Biến lưu giá trị đọc từ cảm biến

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== ESP32 FSR 402 Force Sensor Test ===");
}

void loop() {
  // Đọc giá trị Analog từ cảm biến (0 - 4095 trên ESP32 12-bit ADC)
  fsrReading = analogRead(fsrPin);
  
  // In giá trị ra Serial Monitor
  Serial.print("FSR Analog Reading: ");
  Serial.print(fsrReading);
  
  // Phân loại mức lực cơ bản để giảng viên dễ quan sát
  if (fsrReading < 100) {
    Serial.println(" -> Không có lực (0N)");
  } else if (fsrReading >= 100 && fsrReading < 1000) {
    Serial.println(" -> Lực nhẹ (Nhẹ nhàng)");
  } else if (fsrReading >= 1000 && fsrReading < 2500) {
    Serial.println(" -> Lực trung bình (Đang cầm vật)");
  } else {
    Serial.println(" -> Lực mạnh (Bóp chặt)");
  }
  
  delay(200); // Đọc mỗi 200ms
}
