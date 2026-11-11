# Báo cáo tiến độ firmware – Robot Hand 5 Servo

## 1. Mục tiêu
Xây dựng firmware điều khiển 5 servo quay liên tục của bàn tay robot thông qua ESP32 và module PCA9685. Mỗi servo có chu trình đóng/mở và thời gian hoạt động riêng; có thể điều khiển độc lập hoặc đồng thời theo nhóm.

## 2. Phần cứng và cấu hình
- Vi điều khiển: ESP32-WROOM.
- Driver PWM: PCA9685, địa chỉ I2C `0x40`.
- SDA: GPIO21; SCL: GPIO22.
- Tần số PWM: 50 Hz.
- Servo: 5 MG996R continuous-rotation, kết nối các kênh CH0–CH4.
- Thứ tự kênh: vàng CH0, đỏ CH1, xanh lá CH2, cam CH3, nâu CH4.
- Nguồn servo cần là nguồn ngoài đủ dòng; nối chung GND nguồn servo, PCA9685 và ESP32. Không cấp nguồn cho cả 5 servo từ chân 5V của ESP32.

## 3. Bảng hiệu chuẩn xung

| Servo | Kênh | Quay thuận (µs) | Dừng (µs) | Quay ngược (µs) |
|---|---:|---:|---:|---:|
| Vàng | 0 | 1800 | 1600 | 1200 |
| Đỏ | 1 | 1200 | 1700 | 1800 |
| Xanh lá | 2 | 1200 | 1700 | 1800 |
| Cam | 3 | 2100 | 1700 | 1200 |
| Nâu | 4 | 2100 | 1700 | 1200 |

Các giá trị trên là kết quả hiệu chuẩn thực nghiệm riêng cho từng servo. Xung dừng có thể khác nhau giữa các servo và cần được giữ độc lập trong cấu hình.

## 4. Bảng thời gian chu trình

| Servo | Đóng – xung | Thời gian đóng | Mở – xung | Thời gian mở |
|---|---:|---:|---:|---:|
| Vàng | 1800 µs | 50 s | 1200 µs | 10 s |
| Đỏ | 1800 µs | 6 s | 1200 µs | 2 s |
| Xanh lá | 1800 µs | 10 s | 1200 µs | 4 s |
| Cam | 2100 µs | 4 s | 1200 µs | 4 s |
| Nâu | 2100 µs | 10 s | 1200 µs | 8 s |

Thời gian trên được đo khi thử từng servo riêng lẻ. Cần kiểm tra và tinh chỉnh lại khi lắp đủ tải cơ khí và chạy đồng thời.

## 5. Kiến trúc firmware

Firmware sử dụng state machine không chặn (non-blocking) dựa trên `millis()`.

Mỗi servo có ba trạng thái:
- `IDLE`: servo được phát xung dừng.
- `CLOSING`: servo chạy theo xung và thời gian đóng riêng.
- `OPENING`: servo chạy theo xung và thời gian mở riêng.

Mỗi servo có cấu hình độc lập gồm kênh PCA9685, xung đóng, thời gian đóng, xung mở, thời gian mở và xung dừng. Biến thời gian bắt đầu được lưu riêng cho từng servo.

Trong `loop()`, chương trình liên tục:
1. Đọc lệnh Serial.
2. Cập nhật trạng thái và thời gian của cả 5 servo.
3. Khi thời gian của một servo kết thúc, chỉ servo đó được chuyển về `IDLE` và phát xung dừng.

Nhờ vậy, các servo có thể bắt đầu và kết thúc ở những thời điểm khác nhau mà không phải chờ nhau. Không dùng `delay()` để tạo thời gian chạy servo trong vòng lặp chính.

## 6. Lệnh điều khiển Serial

Thiết lập Serial Monitor: **115200 baud**, chọn kết thúc dòng **Newline**.

| Servo | Đóng | Mở | Dừng |
|---|---|---|---|
| Vàng | `YC` | `YO` | `YS` |
| Đỏ | `RC` | `RO` | `RS` |
| Xanh lá | `GC` | `GO` | `GS` |
| Cam | `OC` | `OO` | `OS` |
| Nâu | `BC` | `BO` | `BS` |

Lệnh nhóm:
- `ALLC`: bắt đầu đóng cả 5 servo.
- `ALLO`: bắt đầu mở cả 5 servo.
- `ALLS`: dừng cả 5 servo.
- `STATUS`: in trạng thái hiện tại của từng servo.

Khi gửi lệnh mới cho một servo đang chạy, trạng thái và mốc thời gian của servo đó được cập nhật theo lệnh mới.

## 7. Lưu ý kỹ thuật
- MG996R continuous-rotation không điều khiển vị trí góc như servo 180°. Xung PWM điều khiển chiều/tốc độ; thời gian chạy chỉ ước lượng hành trình.
- Firmware hiện chưa có cảm biến phản hồi vị trí hoặc phát hiện kẹt ngón tay. Nếu cơ cấu bị cản, chương trình vẫn kết thúc theo thời gian đã đặt.
- Cần thử nghiệm với cơ cấu không tải trước, sau đó tăng dần tải; chuẩn bị nút ngắt nguồn servo khi kiểm thử.
- Nếu servo vẫn quay khi đã phát xung dừng, cần hiệu chuẩn lại xung dừng của chính servo đó.
- `delay(10)` trong `setup()` chỉ dùng sau khi khởi tạo tần số PCA9685; vòng lặp điều khiển không sử dụng delay chặn.

## 8. Tiến độ và công việc tiếp theo

### Đã triển khai trong firmware
- [x] Khai báo cấu hình riêng cho 5 servo.
- [x] Lưu xung đóng/mở/dừng riêng từng servo.
- [x] Tạo state machine `IDLE`, `CLOSING`, `OPENING`.
- [x] Sử dụng `millis()` để quản lý thời gian độc lập.
- [x] Điều khiển từng servo qua Serial.
- [x] Điều khiển nhóm và truy vấn trạng thái.

### Cần kiểm thử/hoàn thiện
- [ ] Nạp firmware và xác nhận đúng thứ tự kênh.
- [ ] Kiểm tra xung dừng của cả 5 servo khi lắp trên cơ cấu.
- [ ] Đo lại thời gian đóng/mở khi chịu tải thực tế.
- [ ] Kiểm tra nhiều lệnh đến liên tiếp và lệnh ghi đè khi servo đang chạy.
- [ ] Kiểm tra sụt áp, nhiễu nguồn và độ ổn định khi 5 servo hoạt động đồng thời.
- [ ] Tích hợp lệnh điều khiển từ giao diện/phần mềm cấp cao.

---
*Tài liệu phản ánh cấu hình và số liệu thử nghiệm hiện có; cần cập nhật sau các lần kiểm thử cơ khí tiếp theo.*
