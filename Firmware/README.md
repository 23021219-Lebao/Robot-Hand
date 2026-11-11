# Robot Hand – ESP32 + PCA9685 (5 Servos)

Firmware điều khiển 5 servo quay liên tục MG996R bằng ESP32 và PCA9685.

## Phần cứng
- ESP32-WROOM
- PCA9685, I2C address `0x40`
- 5 MG996R continuous-rotation
- SDA GPIO21, SCL GPIO22
- PWM 50 Hz
- Servo channels: Yellow CH0, Red CH1, Green CH2, Orange CH3, Brown CH4

**Nguồn:** cấp servo bằng nguồn ngoài đủ dòng. Nối chung GND giữa nguồn servo, PCA9685 và ESP32. Không cấp 5 servo trực tiếp từ ESP32.

## Cài đặt
1. Mở `Firmware_5Servo.ino` bằng Arduino IDE.
2. Cài thư viện **Adafruit PWM Servo Driver Library**.
3. Chọn board ESP32 phù hợp và cổng COM.
4. Kiểm tra dây nguồn, GND chung và thứ tự kênh.
5. Nạp chương trình.
6. Mở Serial Monitor ở 115200 baud, line ending `Newline`.

## Lệnh Serial

| Servo | Close | Open | Stop |
|---|---|---|---|
| Yellow | `YC` | `YO` | `YS` |
| Red | `RC` | `RO` | `RS` |
| Green | `GC` | `GO` | `GS` |
| Orange | `OC` | `OO` | `OS` |
| Brown | `BC` | `BO` | `BS` |

- `ALLC`: đóng tất cả.
- `ALLO`: mở tất cả.
- `ALLS`: dừng tất cả.
- `STATUS`: xem trạng thái.

## Hiệu chuẩn
Xung và thời gian hiện tại nằm trong mảng `servoConfig` ở đầu file `.ino`. Các giá trị là số đo thử nghiệm ban đầu, cần hiệu chỉnh lại theo servo và tải cơ khí thực tế.

Xem `Bao_cao_tien_do_Firmware.md` để biết bảng hiệu chuẩn, chu trình và kiến trúc chương trình.

## Lưu ý
Đây là servo quay liên tục: xung điều khiển chiều/tốc độ, không phải góc đặt chính xác. Điều khiển theo thời gian không thay thế được cảm biến phản hồi vị trí.
