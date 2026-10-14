import sys
sys.stdout.reconfigure(encoding='utf-8')
import pybullet as p
import os

cid = p.connect(p.DIRECT)
urdf_path = "robot_hand.urdf"
robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
print("Loaded robot id:", robot_id)

num_joints = p.getNumJoints(robot_id)
print("Total joints:", num_joints)
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    j_name = info[1].decode("utf-8")
    j_type = info[2]
    print(f"Joint {i}: {j_name}, type={j_type}")

p.stepSimulation()
print("Simulation step SUCCESS!")
p.disconnect()
