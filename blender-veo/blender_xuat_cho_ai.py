"""
Blender -> AI video (Veo 3 / Wan VACE)
Chạy trong Blender: tab Scripting -> Open file này -> Run Script
(hoặc nhờ Claude qua Blender MCP chạy nội dung file).

Xuất ra thư mục OUT_DIR:
  keyframes/<TênCamera>.png          ảnh khung đầu cho Veo 3 (mỗi camera 1 ảnh)
  anim/rgb/####.png                 chuyển động camera đang active (cho Wan VACE)
  anim/depth/####.png               depth map tương ứng (video điều khiển VACE)
"""
import bpy, os

OUT_DIR   = bpy.path.abspath("//ai_export")   # cạnh file .blend
RES       = (1280, 720)                        # Veo: 16:9. Dọc 9:16 thì đổi (720, 1280)
VACE_RES  = (832, 480)                         # Wan VACE 1.3B chạy tốt ở 480p
FPS_VACE  = 16                                 # Wan chạy 16 fps
MAX_FRAMES = 81                                # Wan: số khung = 4n+1, 81 = ~5 giây
SAMPLES   = 64                                 # Cycles samples (tăng nếu cần đẹp hơn)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = "PNG"

def set_res(wh):
    scene.render.resolution_x, scene.render.resolution_y = wh
    scene.render.resolution_percentage = 100

# ---------- 1) Keyframe tĩnh từ mọi camera (cho Veo 3) ----------
os.makedirs(os.path.join(OUT_DIR, "keyframes"), exist_ok=True)
set_res(RES)
active_cam = scene.camera
for cam in [o for o in scene.objects if o.type == "CAMERA"]:
    scene.camera = cam
    scene.render.filepath = os.path.join(OUT_DIR, "keyframes", f"{cam.name}.png")
    bpy.ops.render.render(write_still=True)
    print("Keyframe:", cam.name)
scene.camera = active_cam

# ---------- 2) Chuyển động camera + depth (cho Wan VACE) ----------
set_res(VACE_RES)
orig = (scene.frame_start, scene.frame_end, scene.render.fps)
scene.render.fps = FPS_VACE
scene.frame_end = min(scene.frame_end, scene.frame_start + MAX_FRAMES - 1)

view_layer = bpy.context.view_layer
view_layer.use_pass_mist = True
world = scene.world
world.mist_settings.start = 0.0
world.mist_settings.depth = 25.0   # chỉnh theo kích thước cảnh (mét)

scene.use_nodes = True
tree = scene.node_tree
for n in list(tree.nodes):
    if n.bl_idname == "CompositorNodeOutputFile" and n.label == "AI_DEPTH":
        tree.nodes.remove(n)
rl = next((n for n in tree.nodes if n.bl_idname == "CompositorNodeRLayers"), None) \
     or tree.nodes.new("CompositorNodeRLayers")
inv = tree.nodes.new("CompositorNodeInvert")          # gần = sáng, xa = tối (chuẩn depth)
out = tree.nodes.new("CompositorNodeOutputFile")
out.label = "AI_DEPTH"
out.base_path = os.path.join(OUT_DIR, "anim", "depth")
out.format.file_format = "PNG"
out.format.color_mode = "BW"
tree.links.new(rl.outputs["Mist"], inv.inputs["Color"])
tree.links.new(inv.outputs["Color"], out.inputs[0])

scene.render.filepath = os.path.join(OUT_DIR, "anim", "rgb", "")
bpy.ops.render.render(animation=True)

scene.frame_start, scene.frame_end, scene.render.fps = orig
print("Xong. Thư mục:", OUT_DIR)
