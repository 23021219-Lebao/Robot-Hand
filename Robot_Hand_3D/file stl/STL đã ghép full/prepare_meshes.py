import glob
import os
import shutil
import re

# Mapping dictionary for clean naming without Vietnamese accents and special characters
# PyBullet / URDF often have issues with non-ASCII or spaces in mesh paths.
mapping = {
    "Cả bàn tay - Bantay-1.STL": "palm.stl",
    
    # Thumb (Ngón cái): Đuôi ngón tay-10, Part1-8, Part3-6
    "Cả bàn tay - Đuôi ngón tay-10.STL": "thumb_proximal.stl",
    "Cả bàn tay - Part1-8.STL": "thumb_intermediate.stl",
    "Cả bàn tay - Part3-6.STL": "thumb_distal.stl",
    
    # Index finger (Ngón trỏ): Đuôi ngón tay-7, Part1-4, Part2-2, Part3-2
    "Cả bàn tay - Đuôi ngón tay-7.STL": "index_base.stl",
    "Cả bàn tay - Part1-4.STL": "index_proximal.stl",
    "Cả bàn tay - Part2-2.STL": "index_intermediate.stl",
    "Cả bàn tay - Part3-2.STL": "index_distal.stl",
    
    # Middle finger (Ngón giữa): Đuôi ngón tay-9, Part1-3, Part2-1, Part3-1
    "Cả bàn tay - Đuôi ngón tay-9.STL": "middle_base.stl",
    "Cả bàn tay - Part1-3.STL": "middle_proximal.stl",
    "Cả bàn tay - Part2-1.STL": "middle_intermediate.stl",
    "Cả bàn tay - Part3-1.STL": "middle_distal.stl",
    
    # Ring finger (Ngón áp út): Đuôi ngón tay-11, Part1-5, Part2-3, Part3-3
    "Cả bàn tay - Đuôi ngón tay-11.STL": "ring_base.stl",
    "Cả bàn tay - Part1-5.STL": "ring_proximal.stl",
    "Cả bàn tay - Part2-3.STL": "ring_intermediate.stl",
    "Cả bàn tay - Part3-3.STL": "ring_distal.stl",
    
    # Pinky finger (Ngón út): Đuôi ngón tay-8, Part1-6, Part2-4, Part3-4
    "Cả bàn tay - Đuôi ngón tay-8.STL": "pinky_base.stl",
    "Cả bàn tay - Part1-6.STL": "pinky_proximal.stl",
    "Cả bàn tay - Part2-4.STL": "pinky_intermediate.stl",
    "Cả bàn tay - Part3-4.STL": "pinky_distal.stl",
}

# Add servos 1 to 5
for i in range(1, 6):
    mapping[f"Cả bàn tay - MG996R SBORKA-{i} Servo MG996R-1.STL"] = f"servo_{i}_body.stl"
    mapping[f"Cả bàn tay - MG996R SBORKA-{i} Servo MG996R arm01-1.STL"] = f"servo_{i}_arm.stl"
    mapping[f"Cả bàn tay - MG996R SBORKA-{i} Servo MG996R Shaft-1.STL"] = f"servo_{i}_shaft.stl"

mesh_dir = "meshes"
os.makedirs(mesh_dir, exist_ok=True)

for src, dst in mapping.items():
    if os.path.exists(src):
        dst_path = os.path.join(mesh_dir, dst)
        shutil.copyfile(src, dst_path)
        print(f"Copied {src} -> {dst_path}")
    else:
        print(f"NOT FOUND: {src}")

print("Done copying all meshes.")
