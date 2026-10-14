import os
import glob
import struct
import numpy as np
import sys

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

def read_stl_bounds(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(80)
        num_triangles_bytes = f.read(4)
        if len(num_triangles_bytes) < 4:
            return None
        num_triangles = struct.unpack('<I', num_triangles_bytes)[0]
        
        expected_size = 84 + num_triangles * 50
        file_size = os.path.getsize(file_path)
        
        if file_size == expected_size:
            data = f.read()
            triangles = np.frombuffer(data, dtype=[
                ('normal', '<f4', (3,)),
                ('v1', '<f4', (3,)),
                ('v2', '<f4', (3,)),
                ('v3', '<f4', (3,)),
                ('attr', '<u2')
            ])
            vertices = np.vstack([triangles['v1'], triangles['v2'], triangles['v3']])
            min_bound = vertices.min(axis=0)
            max_bound = vertices.max(axis=0)
            center = (min_bound + max_bound) / 2.0
            size = max_bound - min_bound
            return min_bound, max_bound, center, size, num_triangles
        else:
            return None

stl_files = sorted(glob.glob("*.STL"))
print(f"Total STL files: {len(stl_files)}")
results = []
for f in stl_files:
    res = read_stl_bounds(f)
    if res:
        min_b, max_b, c, s, nt = res
        results.append((f, min_b, max_b, c, s, nt))
        print(f"File: {f}")
        print(f"  Min: [{min_b[0]:.2f}, {min_b[1]:.2f}, {min_b[2]:.2f}]")
        print(f"  Max: [{max_b[0]:.2f}, {max_b[1]:.2f}, {max_b[2]:.2f}]")
        print(f"  Center: [{c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f}]")
        print(f"  Size: [{s[0]:.2f}, {s[1]:.2f}, {s[2]:.2f}]")
