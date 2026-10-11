# Từ điển dữ liệu

Hai tệp Excel trong `data/` giữ nguyên tên cột gốc của phần mềm thu thập dữ liệu:

- `Sample_Index`: số thứ tự mẫu.
- `ESP32_Index`: chỉ số mẫu do chương trình trên ESP32 gửi về.
- `Elapsed_Time_ms`: thời gian đã trôi qua, tính bằng mili giây.
- `ADC_Raw`: giá trị ADC thô.
- `Voltage_V`: điện áp được ghi hoặc tính toán.
- `FSR_Resistance_Ohm`: điện trở cảm biến được ghi hoặc tính toán.
- `Calibrated_Force_N`: lực đầu ra do thuật toán hiệu chuẩn trong tệp nguồn tính.
- `Sample_Status`: trạng thái mẫu đo.

Bảng phân tích bổ sung khối lượng chuẩn, lực chuẩn và sai số lực có dấu/tuyệt đối. Cần xác minh phương trình hiệu chuẩn và tải chuẩn trước khi xem các cột sai số là kết quả đánh giá độ chính xác đo lường.
