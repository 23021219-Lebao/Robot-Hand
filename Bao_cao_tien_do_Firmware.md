# Báo cáo tiến độ phát triển Firmware – Bàn tay robot 5 ngón

## 1. Phạm vi công việc

Phần công việc phụ trách: **Firmware** cho đề tài bàn tay robot 5 ngón.

Mục tiêu hiện tại là xây dựng chương trình điều khiển các servo quay liên tục thông qua ESP32 và mạch điều khiển PWM PCA9685. Công việc đang tập trung vào thử nghiệm điều khiển servo, hiệu chuẩn từng servo và chuẩn bị nền tảng cho việc điều khiển từng ngón tay.

## 2. Cấu hình phần cứng và phần mềm

| Thành phần / thông số | Cấu hình |
|---|---|
| Vi điều khiển | ESP32 |
| Mạch điều khiển PWM | PCA9685 |
| Địa chỉ I2C | `0x40` |
| SDA | GPIO 21 |
| SCL | GPIO 22 |
| Tần số PWM | 50 Hz |
| Động cơ | 5 servo MG996R 360° |
| Môi trường lập trình | Arduino IDE |
| Thư viện | `Wire.h`, `Adafruit_PWMServoDriver.h` |
| Kênh đang thử nghiệm trong code | PCA9685 CH0 |

**Lưu ý:** Chương trình hiện tại mới điều khiển CH0. Bảng hiệu chuẩn nhận diện servo theo màu dây tín hiệu; chưa xác nhận đây là thứ tự kết nối cuối cùng trên các kênh PCA9685.

## 3. Kết quả hiệu chuẩn servo

Các servo được thử nghiệm riêng lẻ. Bảng dưới đây tổng hợp các giá trị xung PWM đã ghi nhận.

| Servo (màu dây tín hiệu) | Thuận (µs) | Dừng (µs) | Ngược (µs) |
|---|---:|---:|---:|
| Vàng | 1800 | 1600 | 1200 |
| Đỏ | 1200 | 1700 | 1800 |
| Xanh | 1200 | 1700 | 1800 |
| Cam | 2100 | 1700 | 1200 |
| Nâu | 2100 | 1700 | 1200 |

### Ghi chú hiệu chuẩn

- Các giá trị trên là kết quả thử nghiệm hiện tại.
- Mỗi servo có thông số hiệu chuẩn riêng; không mặc định thông số của servo này áp dụng cho servo khác.
- Với servo quay liên tục, độ rộng xung PWM quyết định chiều quay và tốc độ quay, không điều khiển trực tiếp một góc quay cố định.
- Có thể cần hiệu chỉnh nhỏ quanh giá trị dừng nếu servo vẫn tự quay.

## 4. Chương trình firmware hiện tại

File chương trình Arduino IDE đi kèm báo cáo là:

`Firmware_Test.ino`

Chương trình hiện tại thực hiện lần lượt ba lệnh xung PWM trên PCA9685 CH0:

| Lệnh | Độ rộng xung | Thời gian |
|---|---:|---:|
| Lệnh thứ nhất | 1800 µs | 4 giây |
| Lệnh thứ hai | 1600 µs | 2 giây |
| Lệnh thứ ba | 1200 µs | 5 giây |

### 4.1. Chuyển đổi xung PWM sang ticks

Ở tần số 50 Hz, chu kỳ PWM là 20.000 µs. PCA9685 chia chu kỳ thành 4096 mức. Công thức đang sử dụng:

```cpp
int ticks = pulse * 4096 / 20000;
```

| Độ rộng xung (µs) | Giá trị ticks |
|---:|---:|
| 1800 | 368 |
| 1600 | 327 |
| 1200 | 245 |

Hàm điều khiển hiện tại xuất tín hiệu tới kênh CH0 bằng lệnh:

```cpp
pwm.setPWM(0, 0, ticks);
```

## 5. Tiến độ thực hiện

- [x] Khởi tạo giao tiếp I2C giữa ESP32 và PCA9685.
- [x] Cấu hình địa chỉ PCA9685 `0x40`.
- [x] Thiết lập tần số PWM 50 Hz.
- [x] Xây dựng hàm chuyển đổi độ rộng xung sang giá trị ticks.
- [x] Thử nghiệm điều khiển servo trên kênh CH0.
- [x] Khảo sát giá trị thuận, dừng và ngược cho cả 5 servo.
- [ ] Xác nhận sơ đồ kết nối từng servo với các kênh PCA9685.
- [ ] Mở rộng hàm điều khiển để lựa chọn kênh servo.
- [ ] Xây dựng chức năng điều khiển riêng từng ngón tay.
- [ ] Xây dựng các thao tác phối hợp cho toàn bộ bàn tay.
- [ ] Bổ sung giới hạn thời gian chuyển động và cơ chế dừng an toàn.
- [ ] Tích hợp dữ liệu cảm biến lực để điều chỉnh lực nắm.

## 6. Kế hoạch phát triển tiếp theo

1. Xác nhận servo tương ứng với từng kênh PCA9685.
2. Mở rộng hàm điều khiển để có thể truyền vào kênh servo và giá trị xung PWM.
3. Lưu riêng thông số hiệu chuẩn của từng servo.
4. Xây dựng các thao tác cơ bản: mở, đóng và dừng từng ngón tay.
5. Bổ sung giới hạn thời gian kéo dây nhằm tránh kéo quá mức, tuột vít hoặc đứt dây.
6. Tích hợp phản hồi cảm biến lực sau khi phần điều khiển servo cơ bản ổn định.

## 7. Trạng thái hiện tại

Firmware đang ở giai đoạn **thử nghiệm điều khiển PWM và hiệu chuẩn riêng từng servo**. Cả 5 servo đã có giá trị xung PWM tương ứng với chiều thuận, trạng thái dừng và chiều ngược.

Chương trình hiện tại vẫn là chương trình thử nghiệm một servo trên CH0. Điều khiển nhiều kênh, điều khiển từng ngón tay, phối hợp chuyển động và tích hợp cảm biến lực là các phần dự kiến triển khai tiếp theo.

---

*Tài liệu được cập nhật theo tiến độ thực hiện firmware của đề tài.*
