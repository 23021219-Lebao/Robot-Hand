# Khảo sát cảm biến lực FSR402 — Dự án Bàn tay robot

Thư mục này lưu dữ liệu gốc và kết quả khảo sát sơ bộ cảm biến lực FSR402 sử dụng ESP32 ở hai mức khối lượng chuẩn danh định.

## Phân loại dữ liệu

* **98 g:** `data/FSR402\_98g\_raw.xlsx`
* **250 g:** `data/FSR402\_250g\_raw.xlsx`

Mỗi tệp chứa 1.000 mẫu trong khoảng 10 giây.

## Kết quả chính

|Chỉ số|98 g|250 g|
|-|-:|-:|
|Lực chuẩn danh định|0,9614 N|2,4525 N|
|ADC trung bình|660,63|2043,24|
|Độ lệch chuẩn ADC|94,61|48,25|
|Hệ số biến thiên ADC|14,32%|2,36%|
|Lực đầu ra trung bình theo tệp nguồn|1,2975 N|2,5860 N|
|Sai số tương đối có dấu của lực trung bình so với lực danh định|+34,96%|+5,44%|
|Số mẫu ADC bão hòa|0|0|

## Giới hạn quan trọng

Đây là các lần đo sơ bộ. 1.000 mẫu thu liên tục trong một lần chạy không tương đương 1.000 lần lặp thí nghiệm độc lập. Tệp Excel nguồn chưa mô tả đầy đủ phương trình hiệu chuẩn; vì vậy, các giá trị sai số lực là kết quả so sánh trực tiếp giữa cột lực đầu ra đã hiệu chuẩn trong tệp và lực danh định `m\*g`, chưa phải kết luận độ chính xác đã được kiểm chứng độc lập. Hãy đọc báo cáo đầy đủ trước khi diễn giải kết quả.

## Thành phần trong thư mục

* `data/` — hai tệp dữ liệu gốc của tải 98 g và 250 g.
* `reports/bao\_cao\_khao\_sat\_FSR402.md` — báo cáo tiếng Việt về phương pháp, kết quả, biểu đồ, giới hạn và đề xuất.
* `results/FSR402\_phan\_tich\_hai\_muc\_tai.xlsx` — bảng so sánh, dữ liệu mẫu kèm cột lực chuẩn/sai số và thống kê mô tả.
* `figures/` — các biểu đồ so sánh hai mức tải.
* `data/DATA\_DICTIONARY.md` — giải thích các cột dữ liệu.

