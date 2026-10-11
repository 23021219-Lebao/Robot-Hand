# BÁO CÁO KHẢO SÁT ĐẶC TÍNH VÀ SAI SỐ ĐẦU RA CẢM BIẾN LỰC FSR402

**Dự án:** Bàn tay robot — khảo sát cảm biến lực FSR402  
**Ngày thu thập:** 11/10/2026  
**Nguồn dữ liệu:** Hai file Excel được gán tải chuẩn 98 g và 250 g.

## 1\. Mục tiêu khảo sát

Khảo sát tín hiệu FSR402 ở hai mức tải danh định 98 g và 250 g, thống kê biến thiên ADC/điện áp/điện trở/lực đầu ra, đồng thời so sánh lực được ghi trong file với lực trọng trường danh định tương ứng.

## 2\. Dữ liệu đầu vào

|Tải danh định|File nguồn|Số mẫu|
|-|-|-:|
|98 g|`FSR402\_calibrated\_test\_20261011\_201129(1).xlsx`|1000|
|250 g|`FSR402\_calibrated\_test\_20261011\_201229.xlsx`|1000|



## 3\. Phương pháp xử lý dữ liệu

* Thống kê trung bình, độ lệch chuẩn mẫu, min, median, max, khoảng biến thiên và hệ số biến thiên (CV).
* Lực chuẩn danh định được tính bằng `F = m × g`, với `g = 9.81 m/s²`.
* Sai số có dấu của lực trung bình: `e = F\_trung\_bình\_đo - F\_chuẩn`.
* Sai số tương đối có dấu: `e\_rel (%) = e / F\_chuẩn × 100%`.
* RMSE: căn bậc hai của trung bình bình phương chênh lệch từng mẫu với lực chuẩn danh định.

**Giới hạn diễn giải:** các phép tính sai số lực ở đây chỉ có ý nghĩa nếu cột `Calibrated\_Force\_N` được tính bằng một phương trình hiệu chuẩn có thể áp dụng cho cả hai phép đo và tải chuẩn thực sự phù hợp với từng lần chạy. File Excel không mô tả đầy đủ phương trình hiệu chuẩn, nên kết quả được gọi là sai số so với lực danh định của đầu ra đang ghi, chưa phải xác nhận độ chính xác chuẩn đo lường.

## 4\. Kết quả so sánh hai mức tải

|Chỉ số|98 g|250 g|Đơn vị|
|-|-:|-:|-|
|Lực chuẩn danh định|0.9614|2.4525|N|
|Số mẫu hợp lệ|1000/1000|1000/1000|mẫu|
|Mẫu ADC bão hòa (>=4095)|0|0|mẫu|
|ADC trung bình|660.63|2043.24|counts|
|Độ lệch chuẩn ADC|94.61|48.25|counts|
|Khoảng ADC|381–784|1927–2179|counts|
|CV của ADC|14.32%|2.36%|%|
|Lực đầu ra trung bình|1.2975|2.5860|N|
|Độ lệch chuẩn lực đầu ra|0.0882|0.0450|N|
|CV lực đầu ra|6.80%|1.74%|%|
|Sai số lực trung bình có dấu|+0.3361|+0.1335|N|
|Sai số tương đối có dấu|+34.96%|+5.44%|%|
|RMSE so với lực danh định|0.3475|0.1409|N|

## 5\. Phân tích và nhận xét

1. **Cả hai lần đo đều có 1.000 mẫu hợp lệ theo cột trạng thái.**
2. Ở tải 98 g, ADC trung bình là 660.63 counts, CV 14.32%; ở tải 250 g, ADC trung bình là 2043.24 counts, CV 2.36%. Hai mức tải tạo ra các vùng ADC khác nhau trong dữ liệu thu thập.
3. CV là độ phân tán tương đối của chuỗi mẫu, không tự động đồng nghĩa với sai số chính xác. Độ lệch chuẩn có thể bao gồm nhiễu, thay đổi tải, creep/hysteresis của FSR và trôi theo thời gian.
4. Lực đầu ra trung bình ở lần đo 98 g là 1.2975 N, so với lực danh định 0.9614 N; ở lần đo 250 g là 2.5860 N, so với lực danh định 2.4525 N. Theo phép so sánh trực tiếp này, sai số tương đối có dấu lần lượt là +34.96% và +5.44%. Cần kiểm tra lại hiệu chuẩn trước khi coi đây là sai số đo lường chính thức.
5. Tương quan thời gian–ADC lần lượt là r=0.895 (98 g) và r=0.958 (250 g). Xu hướng theo thời gian cho thấy cần kiểm tra độ ổn định khi giữ tải cố định; tương quan không xác định nguyên nhân vật lý.

## 6\. Biểu đồ

### ADC theo thời gian, so sánh hai tải

!\[ADC vs time](../figures/adc\_vs\_time\_comparison.png)

### Lực đầu ra và lực chuẩn danh định

!\[Force vs reference](../figures/force\_vs\_reference.png)

### Phân bố ADC theo tải

!\[ADC distribution](../figures/adc\_distribution\_comparison.png)

## 7\. Kết luận

Dữ liệu cho thấy FSR402 và chuỗi đo ESP32 tạo ra tín hiệu ADC phân biệt được giữa hai mức tải danh định trong các lần chạy này. Tuy vậy, mỗi tải hiện mới có một lần thu thập liên tục; 1.000 mẫu trong cùng lần chạy không thay thế cho các lần lặp thí nghiệm độc lập. Kết quả hiện phù hợp để ghi nhận **khảo sát sơ bộ về biến thiên tín hiệu và so sánh đầu ra với tải danh định**, chưa đủ để chứng minh độ chính xác hoặc độ lặp lại dài hạn.

## 8\. Đề xuất cải thiện phương pháp đo

1. Ghi lại sơ đồ mạch, điện trở cố định, điện áp tham chiếu ADC và công thức chuyển đổi ADC → điện áp → điện trở → lực.
2. Xác nhận phương trình hiệu chuẩn và hiệu chuẩn bằng nhiều tải chuẩn; không chỉ dùng hai điểm nếu cần độ chính xác tốt.
3. Cố định cơ khí và diện tích đầu tỳ; dùng cơ cấu giữ tải ổn định, không nhấn tay trong khi thu dữ liệu.
4. Chờ cùng một khoảng thời gian sau khi đặt tải; FSR có thể có creep/hysteresis.
5. Thực hiện ít nhất 3–5 lần đo độc lập cho mỗi tải, nhả tải giữa các lần và lưu từng lần đo riêng.
6. Thêm phép đo không tải và các mức tải trung gian; đánh giá cả chu trình tăng tải/giảm tải.
7. Chỉ công bố sai số tuyệt đối/độ chính xác sau khi xác minh tải chuẩn và mô hình hiệu chuẩn.

## 9\. Tệp trong repository

* `data/FSR402\_98g\_raw.xlsx` — dữ liệu nguồn tải 98 g.
* `data/FSR402\_250g\_raw.xlsx` — dữ liệu nguồn tải 250 g.
* `results/FSR402\_phan\_tich\_hai\_muc\_tai.xlsx` — so sánh hai tải, thống kê và dữ liệu thô kèm cột sai số.
* `figures/` — ba biểu đồ so sánh.
* `reports/bao\_cao\_khao\_sat\_FSR402.md` — báo cáo này.

