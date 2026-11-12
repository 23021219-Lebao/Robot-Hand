% --- SCRIPT TỰ ĐỘNG MỞ SIMULINK VÀ KHÔI PHỤC CẤU HÌNH BÀN TAY ROBOT ---
sys = 'robohand'; % Hoặc tên file .slx bạn vừa Save As
load_system(sys);
open_system(sys); % Tự động mở giao diện mô phỏng Simulink
set_param(sys, 'StopTime', 'inf');

% 1. Cài đặt thông số cho các khớp gập ngón tay
khop_gap = {'Revolute_Cai', 'Revolute10', 'Revolute_Giua', 'Revolute5', 'Revolute7', ...
            'Revolute11', 'Revolute6', 'Revolute9', 'Revolute8', ...
            'Revolute12', 'Revolute16', 'Revolute13', 'Revolute15', 'Revolute14'};
for i = 1:length(khop_gap)
    if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', khop_gap{i}))
        set_param([sys '/' khop_gap{i}], 'SpringStiffness', '0.003', 'SpringStiffnessUnits', 'N*m/deg', ...
                                       'DampingCoefficient', '0.001', 'DampingCoefficientUnits', 'N*m/(deg/s)');
    end
end

% 2. Khóa cứng 5 khớp ngang ở gốc
khop_ngang = {'Revolute', 'Revolute1', 'Revolute2', 'Revolute3', 'Revolute4'};
for i = 1:length(khop_ngang)
    if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', khop_ngang{i}))
        set_param([sys '/' khop_ngang{i}], 'SpringStiffness', '10.0', 'SpringStiffnessUnits', 'N*m/deg', ...
                                       'DampingCoefficient', '0.1', 'DampingCoefficientUnits', 'N*m/(deg/s)');
    end
end

% 3. Cập nhật lại hệ số Gain cánh tay đòn và chiều kéo chuẩn
ds_ngon = {'Ngon_1_Cai', 'Ngon_2_Tro', 'Ngon_3_Giua', 'Ngon_4_ApUt', 'Ngon_5_Ut'};
he_so_dot = [-0.009, +0.008, +0.006];
for f = 1:length(ds_ngon)
    for d = 1:3
        g_blk = sprintf('%s/TayDon_%s_Dot%d', sys, ds_ngon{f}, d);
        if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', sprintf('TayDon_%s_Dot%d', ds_ngon{f}, d)))
            set_param(g_blk, 'Gain', num2str(he_so_dot(d)));
        end
    end
end

% Sửa riêng các đốt ngọn bị ngược chiều (Ngón giữa, Ngón áp út và Ngón út)
if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', 'TayDon_Ngon_3_Giua_Dot3'))
    set_param([sys '/TayDon_Ngon_3_Giua_Dot3'], 'Gain', '-0.006');
end
if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', 'TayDon_Ngon_4_ApUt_Dot3'))
    set_param([sys '/TayDon_Ngon_4_ApUt_Dot3'], 'Gain', '0.006');
end
if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', 'TayDon_Ngon_5_Ut_Dot3'))
    set_param([sys '/TayDon_Ngon_5_Ut_Dot3'], 'Gain', '-0.006');
end

disp('Da khoi phuc xong toan bo thiet lap mo phong!');