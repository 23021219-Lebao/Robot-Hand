import os
import numpy as np

# Scale factor: STL units are mm -> URDF standard is meters (scale = 0.001)
# However, if we keep coordinate origin at palm base, let's define joint positions in METERS.

scale = 0.001

# Joint absolute positions in STL frame (mm)
# Fingers: Index, Middle, Ring, Pinky have:
#   Joint 0: base_joint (yaw / abduction-adduction) attached to palm
#   Joint 1: proximal_joint (pitch / flexion-extension) attached to base
#   Joint 2: intermediate_joint (pitch / flexion-extension) attached to proximal
#   Joint 3: distal_joint (pitch / flexion-extension) attached to intermediate

# Centers of joints in mm:
joints_raw = {
    # Index
    'index_base': np.array([70.58, 151.97, 267.34]),
    'index_prox': np.array([40.74, 151.23, 265.66]),
    'index_inter': np.array([20.06, 149.57, 216.56]),
    'index_dist': np.array([18.20, 149.99, 167.47]),

    # Middle
    'middle_base': np.array([69.72, 189.76, 267.34]),
    'middle_prox': np.array([39.12, 189.73, 265.05]),
    'middle_inter': np.array([30.92, 189.92, 214.45]),
    'middle_dist': np.array([47.38, 190.14, 172.02]),

    # Ring
    'ring_base': np.array([71.00, 228.06, 267.34]),
    'ring_prox': np.array([41.85, 229.63, 264.80]),
    'ring_inter': np.array([35.06, 231.96, 214.02]),
    'ring_dist': np.array([56.34, 229.56, 173.12]),

    # Pinky
    'pinky_base': np.array([74.41, 264.79, 267.34]),
    'pinky_prox': np.array([50.54, 272.66, 264.52]),
    'pinky_inter': np.array([45.31, 276.98, 213.71]),
    'pinky_dist': np.array([73.14, 268.63, 179.35]),

    # Thumb:
    'thumb_prox': np.array([148.70, 141.21, 215.57]),
    'thumb_inter': np.array([141.16, 135.86, 185.14]),
    'thumb_dist': np.array([92.47, 144.56, 158.15]),
}

# In URDF, child origin xyz is relative to parent frame!
# If each link has its visual mesh with origin = -abs_joint_pos, then each link coordinate frame is centered at its parent joint!
# Let's verify:
# Link 0 (palm): origin at [0,0,0], visual origin at [0,0,0].
# Joint base: xyz = abs_pos(base) * scale relative to palm.
# Link base: visual origin = -abs_pos(base) * scale!
# Then child joint prox: xyz = (abs_pos(prox) - abs_pos(base)) * scale!
# Link prox: visual origin = -abs_pos(prox) * scale!
# And so on! This is mathematically 100% exact and preserves the exact SolidWorks CAD assembly alignment!

def format_xyz(v):
    return f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}"

urdf = """<?xml version="1.0" encoding="utf-8"?>
<robot name="robot_hand">

  <material name="palm_mat">
    <color rgba="0.25 0.28 0.32 1.0"/>
  </material>
  <material name="finger_mat">
    <color rgba="0.15 0.55 0.85 1.0"/>
  </material>
  <material name="joint_mat">
    <color rgba="0.9 0.45 0.1 1.0"/>
  </material>
  <material name="servo_mat">
    <color rgba="0.1 0.1 0.1 1.0"/>
  </material>

  <!-- BASE LINK / PALM -->
  <link name="palm_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/palm.stl" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="palm_mat"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/palm.stl" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0.237 0.205 0.289" rpy="0 0 0"/>
      <mass value="0.8"/>
      <inertia ixx="0.002" ixy="0" ixz="0" iyy="0.002" iyz="0" izz="0.002"/>
    </inertial>
  </link>
"""

# Helper to generate 4-DOF finger
def add_4dof_finger(name, mat_color, base_p, prox_p, inter_p, dist_p, mesh_names):
    global urdf
    # 1. Base joint: connects palm -> base_link (abduction/adduction or swivel)
    # Axis along Z or X: In this CAD, palm faces roughly Z/X. Let's make joint axis along Z or Y
    j_base_rel = base_p * scale
    v_base = -base_p * scale
    
    j_prox_rel = (prox_p - base_p) * scale
    v_prox = -prox_p * scale
    
    j_inter_rel = (inter_p - prox_p) * scale
    v_inter = -inter_p * scale
    
    j_dist_rel = (dist_p - inter_p) * scale
    v_dist = -dist_p * scale
    
    m_base, m_prox, m_inter, m_dist = mesh_names
    
    urdf += f"""
  <!-- ==================== {name.upper()} FINGER ==================== -->
  <!-- Base link & joint (Yaw / Abduction) -->
  <link name="{name}_base_link">
    <visual>
      <origin xyz="{format_xyz(v_base)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_base}" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="joint_mat"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_base)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_base}" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.05"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="{name}_yaw_joint" type="revolute">
    <parent link="palm_link"/>
    <child link="{name}_base_link"/>
    <origin xyz="{format_xyz(j_base_rel)}" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.35" upper="0.35" effort="5.0" velocity="3.0"/>
  </joint>

  <!-- Proximal link & joint (Flexion 1) -->
  <link name="{name}_proximal_link">
    <visual>
      <origin xyz="{format_xyz(v_prox)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_prox}" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="{mat_color}"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_prox)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_prox}" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.05"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="{name}_proximal_joint" type="revolute">
    <parent link="{name}_base_link"/>
    <child link="{name}_proximal_link"/>
    <origin xyz="{format_xyz(j_prox_rel)}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.2" upper="1.57" effort="5.0" velocity="3.0"/>
  </joint>

  <!-- Intermediate link & joint (Flexion 2) -->
  <link name="{name}_intermediate_link">
    <visual>
      <origin xyz="{format_xyz(v_inter)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_inter}" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="{mat_color}"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_inter)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_inter}" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.04"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="{name}_intermediate_joint" type="revolute">
    <parent link="{name}_proximal_link"/>
    <child link="{name}_intermediate_link"/>
    <origin xyz="{format_xyz(j_inter_rel)}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0.0" upper="1.57" effort="5.0" velocity="3.0"/>
  </joint>

  <!-- Distal link & joint (Flexion 3) -->
  <link name="{name}_distal_link">
    <visual>
      <origin xyz="{format_xyz(v_dist)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_dist}" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="{mat_color}"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_dist)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/{m_dist}" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.03"/>
      <inertia ixx="0.00005" ixy="0" ixz="0" iyy="0.00005" iyz="0" izz="0.00005"/>
    </inertial>
  </link>

  <joint name="{name}_distal_joint" type="revolute">
    <parent link="{name}_intermediate_link"/>
    <child link="{name}_distal_link"/>
    <origin xyz="{format_xyz(j_dist_rel)}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0.0" upper="1.57" effort="5.0" velocity="3.0"/>
  </joint>
"""

# Add Index
add_4dof_finger('index', 'finger_mat',
                joints_raw['index_base'], joints_raw['index_prox'], joints_raw['index_inter'], joints_raw['index_dist'],
                ['index_base.stl', 'index_proximal.stl', 'index_intermediate.stl', 'index_distal.stl'])

# Add Middle
add_4dof_finger('middle', 'finger_mat',
                joints_raw['middle_base'], joints_raw['middle_prox'], joints_raw['middle_inter'], joints_raw['middle_dist'],
                ['middle_base.stl', 'middle_proximal.stl', 'middle_intermediate.stl', 'middle_distal.stl'])

# Add Ring
add_4dof_finger('ring', 'finger_mat',
                joints_raw['ring_base'], joints_raw['ring_prox'], joints_raw['ring_inter'], joints_raw['ring_dist'],
                ['ring_base.stl', 'ring_proximal.stl', 'ring_intermediate.stl', 'ring_distal.stl'])

# Add Pinky
add_4dof_finger('pinky', 'finger_mat',
                joints_raw['pinky_base'], joints_raw['pinky_prox'], joints_raw['pinky_inter'], joints_raw['pinky_dist'],
                ['pinky_base.stl', 'pinky_proximal.stl', 'pinky_intermediate.stl', 'pinky_distal.stl'])

# Add Thumb (3 DOF)
p_prox = joints_raw['thumb_prox']
p_inter = joints_raw['thumb_inter']
p_dist = joints_raw['thumb_dist']

j_prox_rel = p_prox * scale
v_prox = -p_prox * scale

j_inter_rel = (p_inter - p_prox) * scale
v_inter = -p_inter * scale

j_dist_rel = (p_dist - p_inter) * scale
v_dist = -p_dist * scale

urdf += f"""
  <!-- ==================== THUMB FINGER ==================== -->
  <link name="thumb_proximal_link">
    <visual>
      <origin xyz="{format_xyz(v_prox)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_proximal.stl" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="joint_mat"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_prox)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_proximal.stl" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.06"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="thumb_proximal_joint" type="revolute">
    <parent link="palm_link"/>
    <child link="thumb_proximal_link"/>
    <origin xyz="{format_xyz(j_prox_rel)}" rpy="0 0 0"/>
    <axis xyz="-0.8692 0.4351 0.2350"/>
    <limit lower="-0.3" upper="1.2" effort="5.0" velocity="3.0"/>
  </joint>

  <link name="thumb_intermediate_link">
    <visual>
      <origin xyz="{format_xyz(v_inter)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_intermediate.stl" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="finger_mat"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_inter)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_intermediate.stl" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.05"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="thumb_intermediate_joint" type="revolute">
    <parent link="thumb_proximal_link"/>
    <child link="thumb_intermediate_link"/>
    <origin xyz="{format_xyz(j_inter_rel)}" rpy="0 0 0"/>
    <axis xyz="0.3771 0.8912 -0.2521"/>
    <limit lower="0.0" upper="1.57" effort="5.0" velocity="3.0"/>
  </joint>

  <link name="thumb_distal_link">
    <visual>
      <origin xyz="{format_xyz(v_dist)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_distal.stl" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="finger_mat"/>
    </visual>
    <collision>
      <origin xyz="{format_xyz(v_dist)}" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/thumb_distal.stl" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.04"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="thumb_distal_joint" type="revolute">
    <parent link="thumb_intermediate_link"/>
    <child link="thumb_distal_link"/>
    <origin xyz="{format_xyz(j_dist_rel)}" rpy="0 0 0"/>
    <axis xyz="0.3771 0.8912 -0.2521"/>
    <limit lower="0.0" upper="1.57" effort="5.0" velocity="3.0"/>
  </joint>
"""

# Add Servos on the palm as fixed / rotating links
for i in range(1, 6):
    urdf += f"""
  <!-- Servo {i} -->
  <link name="servo_{i}_body">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/servo_{i}_body.stl" scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="servo_mat"/>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="meshes/servo_{i}_body.stl" scale="0.001 0.001 0.001"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.06"/>
      <inertia ixx="0.00005" ixy="0" ixz="0" iyy="0.00005" iyz="0" izz="0.00005"/>
    </inertial>
  </link>

  <joint name="servo_{i}_fixed_joint" type="fixed">
    <parent link="palm_link"/>
    <child link="servo_{i}_body"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
"""

urdf += "</robot>\n"

with open("robot_hand.urdf", "w", encoding="utf-8") as f:
    f.write(urdf)

print("robot_hand.urdf generated successfully!")
