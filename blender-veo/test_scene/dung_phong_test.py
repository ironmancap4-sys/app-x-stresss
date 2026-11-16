"""Dựng phòng test có vật mốc (cửa sổ, ghế đỏ, tranh, chậu cây, đèn) + Cam_A, Cam_B, render keyframe."""
import bpy, math, os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyframes")
SAMPLES = int(os.environ.get("SAMPLES", "64"))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, color, rough=0.6, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = 8
    return m

def box(name, loc, size, m, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = [s/2 for s in size]; o.data.materials.append(m); return o

def cyl(name, loc, r, d, m):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, vertices=48)
    o = bpy.context.object; o.name = name; o.data.materials.append(m); return o

wall, floor, ceil = mat("Tuong", (0.82,0.78,0.70)), mat("San_go", (0.35,0.20,0.10), 0.4), mat("Tran", (0.9,0.9,0.9))
red, wood, frame = mat("Ghe_do", (0.65,0.04,0.03), 0.5), mat("Go", (0.25,0.14,0.07), 0.5), mat("Khung", (0.05,0.05,0.05), 0.3)
paint = mat("Tranh", (0.10,0.30,0.65), 0.7); green = mat("La", (0.08,0.35,0.10), 0.7); pot = mat("Chau", (0.85,0.45,0.25))
glass = mat("Kinh", (0.8,0.9,1.0), 0.0, emit=(0.85,0.92,1.0))

W, D, H = 6, 5, 3   # phòng 6m x 5m x 3m
box("San", (0,0,-0.05), (W,D,0.1), floor); box("Tran", (0,0,H+0.05), (W,D,0.1), ceil)
box("Tuong_sau", (0, D/2, H/2), (W,0.1,H), wall); box("Tuong_trai", (-W/2,0,H/2), (0.1,D,H), wall)
box("Tuong_phai", (W/2,0,H/2), (0.1,D,H), wall); box("Tuong_truoc", (0,-D/2,H/2), (W,0.1,H), wall)
# Cửa sổ trên tường trái (phát sáng như ánh trời) + khung
box("Cua_so", (-W/2+0.06, 0.3, 1.6), (0.02,1.6,1.4), glass)
box("Khung_ngang", (-W/2+0.08, 0.3, 1.6), (0.04,1.6,0.06), frame); box("Khung_doc", (-W/2+0.08, 0.3, 1.6), (0.04,0.06,1.4), frame)
# Tranh trên tường sau
box("Tranh_khung", (0.8, D/2-0.06, 1.7), (1.3,0.04,0.9), frame); box("Tranh", (0.8, D/2-0.085, 1.7), (1.18,0.02,0.78), paint)
# Ghế đỏ (bành) giữa phòng
box("Ghe_ngoi", (0.6,0.9,0.25), (0.9,0.85,0.5), red); box("Ghe_tua", (0.6,1.25,0.7), (0.9,0.2,0.6), red)
box("Ghe_tay_T", (0.1,0.9,0.45), (0.15,0.85,0.4), red); box("Ghe_tay_P", (1.1,0.9,0.45), (0.15,0.85,0.4), red)
# Bàn gỗ tròn
cyl("Ban_mat", (-0.7,0.3,0.55), 0.45, 0.05, wood); cyl("Ban_chan", (-0.7,0.3,0.27), 0.05, 0.55, wood)
# Chậu cây góc phải
cyl("Chau", (2.4,2.0,0.25), 0.25, 0.5, pot)
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, location=(2.4,2.0,1.0), subdivisions=3); bpy.context.object.data.materials.append(green)
# Đèn trần
cyl("Den", (0,0.5,H-0.15), 0.25, 0.1, mat("Den", (1,1,1), 0.5, emit=(1.0,0.85,0.6)))

# Ánh sáng: nắng qua cửa sổ + area light trần + world
bpy.ops.object.light_add(type="AREA", location=(-W/2-0.3, 0.3, 1.6), rotation=(0, math.radians(90), 0))
L = bpy.context.object.data; L.energy = 1500; L.size = 1.6; L.color = (1.0,0.95,0.88)
bpy.ops.object.light_add(type="AREA", location=(0,0,H-0.05)); bpy.context.object.data.energy = 300; bpy.context.object.data.size = 3
sc.world = bpy.data.worlds.new("W"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.3

def cam(name, loc, target):
    bpy.ops.object.camera_add(location=loc); c = bpy.context.object; c.name = name; c.data.lens = 24
    d = [t-l for t,l in zip(target, loc)]
    c.rotation_euler = (math.atan2(math.hypot(d[0],d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi/2); return c
cam("Cam_A", (0.2,-2.2,1.5), (0,1.5,1.1))      # nhìn thẳng vào tường sau
cam("Cam_B", (2.3,-1.6,1.5), (-0.6,1.4,1.0))   # lệch phải ~35°, nhìn chéo về cửa sổ

sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.view_settings.view_transform = "AgX"
os.makedirs(OUT, exist_ok=True)
for n in ("Cam_A", "Cam_B"):
    sc.camera = bpy.data.objects[n]; sc.render.filepath = os.path.join(OUT, f"{n}.png")
    bpy.ops.render.render(write_still=True); print("Rendered", n)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "phong_test.blend"))
