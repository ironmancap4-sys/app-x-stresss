#!/usr/bin/env python3
"""Trộn giọng đọc + SFX và chuẩn hoá loudness cho video mạng xã hội.

  python mix_audio.py voice.mp3 events.json out.wav [--sfx-below 14] [--lufs -14] [--tp -1]

events.json: [{"t": 27.9, "sfx": "whoosh.wav"}, {"t": 37.9, "sfx": "pop.wav", "db": -2}, ...]
  - "t" giây trên trục thời gian video; "db" chỉnh thêm cho riêng sự kiện (mặc định 0).
  - Mức SFX tự đặt = loudness giọng đọc − sfx-below (mặc định 14 dB, yêu cầu ≥ 12 dB).
Kết quả: WAV 48 kHz stereo, đã loudnorm 2 lượt về -14 LUFS, true peak ≤ -1 dBTP; in ra số đo kiểm chứng.
Cần ffmpeg, numpy.
"""
import argparse, json, re, subprocess, sys, wave
import numpy as np

SR = 48000

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)

def decode(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def lufs_of(x):
    """Loudness tích hợp (LUFS) của mảng stereo, qua ffmpeg ebur128. Âm ngắn < 0,4 s: lặp lại để đo được."""
    if len(x) < SR * 3:
        reps = int(np.ceil(SR * 3 / max(len(x), 1)))
        x = np.concatenate([np.concatenate([x, np.zeros((SR // 2, 2), np.float32)])] * reps)
    p = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-af", "ebur128=peak=true", "-f", "null", "-"], input=x.astype(np.float32).tobytes(),
                       capture_output=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr.decode())
    return float(m[-1]) if m else -70.0

def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice"); ap.add_argument("events"); ap.add_argument("out")
    ap.add_argument("--sfx-below", type=float, default=14.0)
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-1.0)
    ap.add_argument("--duration", type=float, default=None, help="độ dài video (s); mặc định = giọng đọc")
    a = ap.parse_args()

    vo = decode(a.voice)
    n = int(SR * a.duration) if a.duration else len(vo)
    mix = np.zeros((max(n, len(vo)), 2), np.float32)
    mix[:len(vo)] += vo
    L_vo = lufs_of(vo)
    target_sfx = L_vo - a.sfx_below
    events = json.load(open(a.events, encoding="utf-8"))
    base = a.events.rsplit("/", 1)[0] + "/" if "/" in a.events else ""
    cache = {}
    for e in events:
        f = e["sfx"] if e["sfx"].startswith("/") else base + e["sfx"]
        if f not in cache:
            s = decode(f); cache[f] = (s, lufs_of(s))
        s, L = cache[f]
        g = 10 ** ((target_sfx - L + e.get("db", 0)) / 20)
        i = int(e["t"] * SR)
        j = min(len(mix), i + len(s))
        if i < len(mix):
            mix[i:j] += s[: j - i] * g
    mix = mix[:n] if a.duration else mix
    tmp = a.out + ".pre.wav"
    write_wav(tmp, mix / max(1.0, float(np.max(np.abs(mix)))))

    # loudnorm 2 lượt
    p = run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:print_format=json", "-f", "null", "-"])
    st = json.loads(re.findall(r"\{[^{}]+\}", p.stderr)[-1])
    af = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
          f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true,"
          f"alimiter=limit={10 ** ((a.tp - 0.3) / 20):.4f}:level=disabled")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", af, "-ar", str(SR), a.out])
    # đo kiểm chứng
    p = run(["ffmpeg", "-hide_banner", "-i", a.out, "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", p.stderr)[-1]
    TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", p.stderr)[-1]
    print(f"giọng đọc {L_vo:.1f} LUFS | SFX đặt ở {target_sfx:.1f} LUFS (thấp hơn {a.sfx_below} dB) | {len(events)} sự kiện")
    print(f"KẾT QUẢ: {I} LUFS, true peak {TP} dBTP -> {a.out}")
    if float(I) < a.lufs - 1 or float(I) > a.lufs + 1 or float(TP) > a.tp:
        print("CẢNH BÁO: chưa đạt chuẩn loudness", file=sys.stderr); sys.exit(2)

if __name__ == "__main__":
    main()
