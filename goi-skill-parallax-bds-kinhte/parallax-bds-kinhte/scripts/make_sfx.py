#!/usr/bin/env python3
"""Tạo SFX tổng hợp, tất định, không bản quyền: whoosh, pop, riser (48 kHz, stereo WAV)."""
import numpy as np, wave, sys, os
SR = 48000
rng = np.random.default_rng(7)
def write(name, x):
    x = np.clip(x / (np.max(np.abs(x)) + 1e-9) * 0.89, -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
def onepole_lp(x, fc):  # fc: mảng tần số cắt theo thời gian
    y = np.zeros_like(x); a = np.exp(-2 * np.pi * fc / SR); s = 0.0
    for i in range(len(x)):
        s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y
def whoosh(dur=0.55):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    fc = 300 + 5200 * np.sin(np.pi * t) ** 2          # quét lên rồi xuống
    lp = onepole_lp(noise, fc); hp = lp - onepole_lp(lp, np.full(n, 180.0))
    env = np.sin(np.pi * t) ** 1.6
    pan = np.sin(np.pi * t)
    x = hp * env
    return np.stack([x * (1.1 - pan * 0.5), x * (0.6 + pan * 0.5)], 1)
def pop(dur=0.12):
    n = int(SR * dur); t = np.arange(n) / SR
    f = 1250 * np.exp(-t * 28) + 420
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 38) + 0.25 * rng.standard_normal(n) * np.exp(-t * 300)
def riser(dur=1.4):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    f = 180 * (2 ** (t * 2.6)); ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.4 * np.sin(2 * ph)
    noise = onepole_lp(rng.standard_normal(n), 400 + 6000 * t ** 2)
    env = t ** 2.2
    return (0.55 * tone + 0.8 * noise) * env
os.makedirs("out", exist_ok=True)
write("out/whoosh.wav", whoosh()); write("out/pop.wav", pop()); write("out/riser.wav", riser())
print("ok")
