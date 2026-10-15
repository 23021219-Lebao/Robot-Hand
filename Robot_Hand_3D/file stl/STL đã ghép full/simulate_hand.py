import sys
import os
import time
import math
import pybullet as p
import pybullet_data

# Force utf-8 output for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def run_simulation():
    # 1. Khởi tạo môi trường đồ hoạ PyBullet GUI
    physicsClient = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    
    # 2. Cấu hình môi trường vật lý
    p.setGravity(0, 0, -9.81)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
    p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
    
    # Nạp sàn mô phỏng
    p.loadURDF("plane.urdf")
    
    # 3. Nạp file URDF bàn tay robot
    urdf_path = "robot_hand.urdf"
    start_pos = [0, 0, 0.5]
    start_orientation = p.getQuaternionFromEuler([0, math.pi/2, 0])  # Dựng đứng bàn tay
    
    robot_id = p.loadURDF(urdf_path, start_pos, start_orientation, useFixedBase=True)
    
    # 4. Cài đặt góc nhìn camera nhìn rõ bàn tay
    p.resetDebugVisualizerCamera(
        cameraDistance=0.55,
        cameraYaw=50,
        cameraPitch=-20,
        cameraTargetPosition=[0.15, 0.1, 0.35]
    )
    
    # 5. Phân loại các khớp
    num_joints = p.getNumJoints(robot_id)
    movable_joints = []
    slider_ids = {}
    
    print("\n" + "="*50)
    print(f" ĐÃ TẢI THÀNH CÔNG BÀN TAY ROBOT VỚI {num_joints} KHỚP")
    print("="*50)
    
    for i in range(num_joints):
        info = p.getJointInfo(robot_id, i)
        j_name = info[1].decode('utf-8')
        j_type = info[2]  # 0: REVOLUTE
        low = info[8]
        high = info[9]
        if j_type == p.JOINT_REVOLUTE:
            movable_joints.append(i)
            # Tạo thanh trượt điều khiển trực tiếp trên UI
            slider_ids[i] = p.addUserDebugParameter(j_name, low, high, 0.0)
            print(f"Khớp [{i:02d}]: {j_name:<26} (Góc: [{low:.2f}, {high:.2f}])")

    print("\n" + "-"*50)
    print(" HƯỚNG DẪN ĐIỀU KHIỂN:")
    print(" 1. Kéo các thanh Slider ở bảng bên phải để chỉnh góc từng khớp.")
    print(" 2. Nhấn phím SPACE để BẬT/TẮT chế độ tự động co/xòe bàn tay.")
    print(" 3. Giữ chuột trái để xoay camera, chuột phải để zoom, chuột giữa để di chuyển.")
    print("-"*50 + "\n")
    
    auto_mode = False
    step = 0
    
    # Vòng lặp mô phỏng thời gian thực
    try:
        while p.isConnected():
            step += 1
            
            # Đọc sự kiện bàn phím
            keys = p.getKeyboardEvents()
            if ord(' ') in keys and (keys[ord(' ')] & p.KEY_WAS_TRIGGERED):
                auto_mode = not auto_mode
                status = "BẬT (Auto Flex/Extend)" if auto_mode else "TẮT (Chế độ thủ công qua Sliders)"
                print(f"[Trạng thái] Tự động cử động: {status}")
                
            if auto_mode:
                # Tạo chuyển động co xòe hình sin mượt mà
                t = step * 0.02
                wave = (math.sin(t) + 1.0) / 2.0  # Chu kỳ 0 -> 1
                
                for j_idx in movable_joints:
                    info = p.getJointInfo(robot_id, j_idx)
                    j_name = info[1].decode('utf-8')
                    low = info[8]
                    high = info[9]
                    
                    if "yaw" in j_name:
                        # Khớp xòe/khép ngón tay
                        target_pos = math.sin(t * 0.5) * 0.15
                    else:
                        # Khớp gập đốt ngón
                        target_pos = low + wave * (high - low) * 0.8
                        
                    p.setJointMotorControl2(
                        robot_id,
                        j_idx,
                        p.POSITION_CONTROL,
                        targetPosition=target_pos,
                        force=15.0
                    )
            else:
                # Đọc giá trị điều khiển từ Slider
                for j_idx, s_id in slider_ids.items():
                    val = p.readUserDebugParameter(s_id)
                    p.setJointMotorControl2(
                        robot_id,
                        j_idx,
                        p.POSITION_CONTROL,
                        targetPosition=val,
                        force=15.0
                    )
                    
            p.stepSimulation()
            time.sleep(1.0 / 240.0)
            
    except KeyboardInterrupt:
        print("\nĐã dừng mô phỏng.")
    finally:
        p.disconnect()

if __name__ == "__main__":
    run_simulation()
