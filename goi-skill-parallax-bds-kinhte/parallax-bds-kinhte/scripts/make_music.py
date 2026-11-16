#!/usr/bin/env python3
"""Nhạc nền beat rõ, tổng hợp tất định (không bản quyền) để dựng theo nhịp.

  python make_music.py out.wav --dur 257.44 [--bpm 100] [--seed 3]

In ra danh sách mốc beat (giây) vào out.beats.json để cắt cảnh/SFX theo nhịp.
Cấu trúc: intro 2 nhịp (pad) -> groove (kick 1&3, clap 2&4, hi-hat 1/8, bass theo hợp âm Am–F–C–G) -> outro nhỏ dần.
"""
import argparse, json, wave
import numpy as np

SR = 48000

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--bpm", type=float, default=100); ap.add_argument("--seed", type=int, default=3)
    a = ap.parse_args(); rng = np.random.default_rng(a.seed)
    n = int(a.dur * SR); L = np.zeros(n); R = np.zeros(n)
    beat = 60 / a.bpm; bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G (MIDI)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def add(sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR); j = min(n, i + len(sig))
        if i >= n or j <= i: return
        L[i:j] += sig[: j - i] * g * (1 - pan) ; R[i:j] += sig[: j - i] * g * (1 + pan)
    kick_n = int(0.35 * SR); tk = np.arange(kick_n) / SR
    kick = np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-tk * 30)) / SR) * env(kick_n, 0.002, 0.12)
    clap_n = int(0.25 * SR); clap = rng.standard_normal(clap_n) * env(clap_n, 0.002, 0.06)
    clap = np.convolve(clap, np.ones(6) / 6, "same")
    hat_n = int(0.06 * SR); hat = np.diff(rng.standard_normal(hat_n + 1)) * env(hat_n, 0.001, 0.015)
    beats = []
    t = 0.0; k = 0
    while t < a.dur:
        b = k % 4; barno = k // 4; intro = barno < 2; outro = t > a.dur - 2 * bar
        beats.append(round(t, 4))
        if not intro:
            g = 0.5 if outro else 1.0
            if b in (0, 2): add(kick, t, 0, 0.9 * g)
            if b in (1, 3): add(clap, t, 0.1, 0.28 * g)
            add(hat, t + beat / 2, -0.3, 0.16 * g); add(hat, t, -0.3, 0.09 * g)
        if b == 0:  # hợp âm + bass mỗi ô nhịp
            ch = chords[barno % 4]; dn = int(bar * SR); tt = np.arange(dn) / SR
            pad = sum(np.sin(2 * np.pi * hz(m) * tt + 0.3 * np.sin(2 * np.pi * 0.2 * tt)) for m in ch) / 3
            pad *= np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.6)
            add(pad, t, 0.0, 0.10)
            if not intro:
                for q in range(8):
                    bn = int(beat / 2 * SR); tb = np.arange(bn) / SR
                    bs = np.tanh(2.2 * np.sin(2 * np.pi * hz(ch[0] - 24) * tb)) * env(bn, 0.004, 0.18)
                    add(bs, t + q * beat / 2, 0, 0.22 * (0.5 if outro else 1))
        t += beat; k += 1
    fade = np.ones(n); fo = int(3 * SR); fade[-fo:] = np.linspace(1, 0, fo); fi = int(1.5 * SR); fade[:fi] = np.linspace(0, 1, fi)
    st = np.stack([L * fade, R * fade], 1); st /= np.max(np.abs(st)) + 1e-9; st *= 0.9
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    json.dump({"bpm": a.bpm, "beats": beats}, open(a.out.rsplit(".", 1)[0] + ".beats.json", "w"))
    print(f"{a.out}: {a.dur:.1f} s, {a.bpm} BPM, {len(beats)} beat")

if __name__ == "__main__":
    main()
