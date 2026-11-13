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
        set_param([sys '/' khop_ngang{i}], 'SpringStiffness', '0.1', 'SpringStiffnessUnits', 'N*m/deg', ...
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

% 4. Thiết lập và điều khiển 5 khớp lắc ngang ở gốc ngón tay
ds_khop_lac   = {'Revolute', 'Revolute1', 'Revolute2', 'Revolute3', 'Revolute4'};
gain_lac      = [ 0.1, -0.1, -0.1, -0.1, -0.1]; % Giữ nguyên chiều ngón cái, đảo chiều 4 ngón còn lại
gioi_han_duoi = [-180,  -25,  -25,  -25,  -30];  % Giới hạn dưới (độ): Cái(-180), Trỏ/Giữa/ÁpÚt(-25), Út(-30)
gioi_han_tren = [ 15,   25,   25,   25,   25];  % Giới hạn trên (độ): Cái(+15), 4 ngón còn lại(+25)

for f = 1:length(ds_ngon)
    ten_ngon = ds_ngon{f};
    ps_dot1 = [sys '/SL2PS_' ten_ngon '_Dot1'];
    
    % Tự động dò từ nhánh Dot1 -> Khớp gập gốc -> Đuôi ngón tay -> Khớp lắc gốc
    khop_lac_tim_thay = '';
    if ~isempty(find_system(sys, 'SearchDepth', 1, 'Name', ['SL2PS_' ten_ngon '_Dot1']))
        pc1 = get_param(ps_dot1, 'PortConnectivity');
        for k1 = 1:length(pc1)
            if ~isempty(pc1(k1).DstBlock)
                b_gap = pc1(k1).DstBlock(1);
                pc2 = get_param(b_gap, 'PortConnectivity');
                for k2 = 1:length(pc2)
                    if ~isempty(pc2(k2).DstBlock)
                        b_duoi = pc2(k2).DstBlock(1);
                        if contains(get_param(b_duoi, 'Name'), 'ui_ngn_tay')
                            pc3 = get_param(b_duoi, 'PortConnectivity');
                            for k3 = 1:length(pc3)
                                if ~isempty(pc3(k3).DstBlock)
                                    ten_b3 = get_param(pc3(k3).DstBlock(1), 'Name');
                                    if ismember(ten_b3, ds_khop_lac)
                                        khop_lac_tim_thay = ten_b3;
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end
    end
    
    if ~isempty(khop_lac_tim_thay)
        duong_dan_k = [sys '/' khop_lac_tim_thay];
        low_val  = gioi_han_duoi(f);
        high_val = gioi_han_tren(f);
        g_val    = gain_lac(f);
        
        % Quy đổi giới hạn góc vật lý trên khớp Revolute theo chiều của Gain
        if g_val > 0
            j_low  = low_val;
            j_high = high_val;
        else
            j_low  = -high_val;
            j_high = -low_val;
        end
        
        % Bật cổng Torque và đặt giới hạn góc lắc vật lý cho từng ngón
        set_param(duong_dan_k, 'TorqueActuationMode', 'InputTorque', ...
                               'MotionActuationMode', 'ComputedMotion', ...
                               'LowerLimitSpecify', 'on', 'LowerLimitBound', num2str(j_low), ...
                               'UpperLimitSpecify', 'on', 'UpperLimitBound', num2str(j_high));
        
        y_pos = 760 + (f-1)*65;
        sl_name = ['Lac_' ten_ngon];
        g_name  = ['Gain_Lac_' ten_ngon];
        ps_name = ['SL2PS_Lac_' ten_ngon];
        
        % Tạo mới nếu chưa có trên sơ đồ
        if isempty(find_system(sys, 'SearchDepth', 1, 'Name', sl_name))
            add_block('simulink/Math Operations/Slider Gain', [sys '/' sl_name], ...
                'low', num2str(low_val), 'gain', '0', 'high', num2str(high_val), 'Position', [-420 y_pos -360 y_pos+30]);
            add_block('simulink/Math Operations/Gain', [sys '/' g_name], ...
                'Gain', num2str(g_val), 'Position', [-260 y_pos -210 y_pos+30]);
            add_block('nesl_utility/Simulink-PS Converter', [sys '/' ps_name], ...
                'Unit', 'N*m', 'Position', [-150 y_pos -120 y_pos+30]);
            
            add_line(sys, 'Nguon_Luc/1', [sl_name '/1'], 'autorouting', 'on');
            add_line(sys, [sl_name '/1'], [g_name '/1'], 'autorouting', 'on');
            add_line(sys, [g_name '/1'], [ps_name '/1'], 'autorouting', 'on');
            
            ph_ps = get_param([sys '/' ps_name], 'PortHandles');
            ph_k  = get_param(duong_dan_k, 'PortHandles');
            add_line(sys, ph_ps.RConn(1), ph_k.LConn(2), 'autorouting', 'on');
        else
            % Nếu đã có sẵn trên sơ đồ thì cập nhật dải trượt và chiều Gain mới
            set_param([sys '/' sl_name], 'low', num2str(low_val), 'gain', '0', 'high', num2str(high_val));
            set_param([sys '/' g_name],  'Gain', num2str(g_val));
        end
    end
end

disp('Da khoi phuc xong toan bo thiet lap mo phong!');