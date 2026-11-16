"""Chạy 3 bài test Veo (T1-T3) từ keyframe Blender. Key do proxy của môi trường chèn vào header x-goog-api-key.
Dùng: python3 chay_test_veo.py [T1 T2 T3]   (mặc định chạy cả 3)
"""
import os, sys, time
from google import genai
from google.genai import types

HERE = os.path.dirname(os.path.abspath(__file__))
KF, OUT = os.path.join(HERE, "keyframes"), os.path.join(HERE, "ket_qua")
MODEL = os.environ.get("VEO_MODEL", "veo-3.1-fast-generate-preview")
os.makedirs(OUT, exist_ok=True)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "dummy-proxy-injects-real-key"))

def img(n): return types.Image(image_bytes=open(os.path.join(KF, n), "rb").read(), mime_type="image/png")

TESTS = {
  "T1": ("Static locked-off camera. Soft daylight slowly shifts across the room, subtle dust in the light. "
         "Photorealistic interior, real fabric and wood materials. Keep every object exactly in place.", "Cam_A.png", None),
  "T2": ("Smooth slow camera dolly moving through the same room from the first view to the second view. "
         "Photorealistic, no new objects, consistent architecture and furniture.", "Cam_A.png", "Cam_B.png"),
  "T3": ("Camera slowly pans 180 degrees to the left to reveal the rest of the room. Photorealistic interior.", "Cam_A.png", None),
}

for name in (sys.argv[1:] or TESTS):
    prompt, first, last = TESTS[name]
    cfg = types.GenerateVideosConfig(aspect_ratio="16:9", last_frame=img(last) if last else None)
    print(f"[{name}] gửi yêu cầu tới {MODEL} ...", flush=True)
    op = client.models.generate_videos(model=MODEL, prompt=prompt, image=img(first), config=cfg)
    while not op.done:
        time.sleep(10); op = client.operations.get(op)
    if op.error or not op.response or not op.response.generated_videos:
        print(f"[{name}] LỖI:", op.error or op.response); continue
    v = op.response.generated_videos[0]
    client.files.download(file=v.video)
    path = os.path.join(OUT, f"{name}.mp4"); v.video.save(path)
    print(f"[{name}] xong -> {path}", flush=True)
