#!/usr/bin/env python3
"""Chép lời tiếng Việt kèm mốc thời gian TỪNG TỪ (để đặt camera/chữ khớp giọng đọc).

  pip install faster-whisper numpy
  python transcribe_vi.py voice.mp3 transcript.json [--model small|medium|<thư mục model CTranslate2>]

Cần ffmpeg. Whisper hay nghe sai tên riêng và số (vd. "sông Tiền" -> "xong tiền", "19,34%" -> "39,34%"):
mọi con số đưa lên màn hình phải đối chiếu với nguồn báo, không lấy từ bản chép lời.
"""
import argparse, json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("out"); ap.add_argument("--model", default="small")
a = ap.parse_args()
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
m = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="vi", word_timestamps=True, beam_size=5)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}", flush=True)
json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
