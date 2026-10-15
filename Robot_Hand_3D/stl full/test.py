import os
import pybullet as p
import pybullet_data
import time
import math

# 1. Kết nối với môi trường mô phỏng PyBullet (Giao diện GUI)
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# 2. Tải mặt phẳng nền và vật thể mẫu (khối lập phương)
planeId = p.loadURDF("plane.urdf")
object_start_pos = [0.1, 0, 0.5]
target_object = p.loadURDF("cube.urdf", basePosition=object_start_pos, globalScaling=0.04)

urdf_path = r"D:\stl full\Assem2.SLDASM\urdf\Assem2.SLDASM.urdf"

# --- CẤU HÌNH VỊ TRÍ VÀ HƯỚNG XOAY ---
hand_start_pos = [0, 0, 0.5] 
roll = 0.0 
pitch = math.pi / 2 
yaw = 0.0 
hand_start_orientation = p.getQuaternionFromEuler([roll, pitch, yaw])

constraints = {}
sliders = {}

try:
    hand_id = p.loadURDF(urdf_path, hand_start_pos, hand_start_orientation, useFixedBase=True)
    print("Đã tải thành công mô hình bàn tay vào PyBullet!")
    
    # --- ĐỔI MÀU ---
    p.changeVisualShape(hand_id, -1, rgbaColor=[0, 0, 0, 1])  # Màu đen cho đế
    
    hand_colors = [
        [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
        [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
        [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
        [1, 1, 1, 1], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
        [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [1, 1, 1, 1]
    ]
    for i, color in enumerate(hand_colors):
        if i < p.getNumJoints(hand_id):
            p.changeVisualShape(hand_id, i, rgbaColor=color)

    # --- DANH SÁCH 5 NGÓN TAY CẦN TẠO DÂY KÉO ---
    finger_names = ["thumb", "index", "middle", "ring", "little"]

    # Tự động quét link và lấy vị trí thực tế của đầu ngón tay trong không gian world
    for finger in finger_names:
        target_link_name = f"{finger}_distal_link"
        link_index = -1
        
        for i in range(p.getNumJoints(hand_id)):
            info = p.getJointInfo(hand_id, i)
            child_link_name = info[12].decode('utf-8')
            if child_link_name == target_link_name:
                link_index = i
                break
        
        if link_index != -1:
            # Lấy tọa độ [x, y, z] thực tế của link đầu ngón tay
            link_state = p.getLinkState(hand_id, link_index)
            link_world_pos = link_state[0]
            
            # Tạo constraint nối từ thế giới vào đúng vị trí thực tế của đầu ngón tay
            cid = p.createConstraint(
                parentBodyUniqueId=hand_id,
                parentLinkIndex=link_index,
                childBodyUniqueId=-1,  
                childLinkIndex=-1,
                jointType=p.JOINT_POINT2POINT,
                jointAxis=[0, 0, 0],
                parentFramePosition=[0, 0, 0],  
                childFramePosition=link_world_pos
            )
            
            constraints[finger] = {
                "id": cid,
                "base_pos": link_world_pos
            }
            
            # Tạo thanh trượt (Slider) trên giao diện GUI
            sliders[finger] = p.addUserDebugParameter(f"Keo day {finger}", 0.0, 0.08, 0.0)
            print(f"Đã tạo điểm kéo cho ngón: {finger} tại tọa độ {link_world_pos}")
        else:
            print(f"Không tìm thấy link: {target_link_name}")
        
except Exception as e:
    print(f"Lỗi khi tải file URDF hoặc cấu hình: {e}")

# Chạy vài bước để hệ thống vật lý ổn định vị trí ban đầu
for _ in range(50):
    p.stepSimulation()

# 4. Vòng lặp mô phỏng đọc giá trị từ thanh trượt
while True:
    for finger, data in constraints.items():
        slider_id = sliders[finger]
        pull_distance = p.readUserDebugParameter(slider_id) # Lấy giá trị thanh trượt
        
        base_pos = data["base_pos"]
        
        # Hướng kéo lùi về phía sau (thay đổi theo trục X và Z của world)
        current_target = [
            base_pos[0] - pull_distance * 0.8, 
            base_pos[1], 
            base_pos[2] - pull_distance * 0.6
        ]
        
        # Cập nhật vị trí điểm kéo và tăng lực maxForce lên 150 để đảm bảo thắng lực cản khớp
        p.changeConstraint(
            data["id"], 
            jointChildPivot=current_target, 
            maxForce=150 
        )

    p.stepSimulation()
    time.sleep(1.0 / 240.0)