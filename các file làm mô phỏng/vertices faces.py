import trimesh

# Tải tệp mô hình 3D của bạn (ví dụ: file.stl hoặc file.obj)
mesh = trimesh.load('C:/Users/hungd/OneDrive/Tài liệu/GitHub/Robot-Hand/Robot_Hand_3D/file stl/stl full/cả bàn - Bantay-1.STL')

# Lấy danh sách toàn bộ các đỉnh (mỗi dòng là một tọa độ [x, y, z])
vertices = mesh.vertices

# Lấy danh sách toàn bộ các mặt (mỗi dòng chứa các chỉ số đỉnh tạo thành mặt tam giác)
faces = mesh.faces

print(f"Số lượng đỉnh: {len(vertices)}")
print(f"Số lượng mặt: {len(faces)}")

# Bạn có thể dùng trực tiếp hai biến `vertices` và `faces` này truyền vào hàm tạo file .obj ở bước trước!