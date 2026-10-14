import trimesh
import numpy as np

def find_revolute_joint(mesh1_path, mesh2_path):
    m1 = trimesh.load(mesh1_path)
    m2 = trimesh.load(mesh2_path)
    
    # Points of mesh1 close to mesh2
    # Find distance between vertices
    p1 = m1.vertices
    p2 = m2.vertices
    
    # Compute bounding boxes intersection
    min_inter = np.maximum(m1.bounds[0], m2.bounds[0])
    max_inter = np.minimum(m1.bounds[1], m2.bounds[1])
    
    center_inter = (min_inter + max_inter) / 2.0
    size_inter = max_inter - min_inter
    
    return center_inter, size_inter, min_inter, max_inter

fingers = {
    'index': ['palm.stl', 'index_base.stl', 'index_proximal.stl', 'index_intermediate.stl', 'index_distal.stl'],
    'middle': ['palm.stl', 'middle_base.stl', 'middle_proximal.stl', 'middle_intermediate.stl', 'middle_distal.stl'],
    'ring': ['palm.stl', 'ring_base.stl', 'ring_proximal.stl', 'ring_intermediate.stl', 'ring_distal.stl'],
    'pinky': ['palm.stl', 'pinky_base.stl', 'pinky_proximal.stl', 'pinky_intermediate.stl', 'pinky_distal.stl'],
    'thumb': ['palm.stl', 'thumb_proximal.stl', 'thumb_intermediate.stl', 'thumb_distal.stl']
}

for f_name, parts in fingers.items():
    print(f"=== {f_name.upper()} FINGER ===")
    for i in range(len(parts)-1):
        c, s, mi, ma = find_revolute_joint(f'meshes/{parts[i]}', f'meshes/{parts[i+1]}')
        print(f"  Joint {parts[i]} -> {parts[i+1]}:")
        print(f"    Inter Center: {c.round(2)}, Size: {s.round(2)}")
        print(f"    Inter Bounds: min={mi.round(2)}, max={ma.round(2)}")
