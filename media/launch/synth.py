#!/usr/bin/env python3
"""Soundtrack for the whatsapp-skills brag video: one piece, one beat grid.

120 BPM (beat 0.5 s, bar 2 s), C major, C-G-Am-F. Music and effects share the
key and the grid; effects sit under the music. Writes audio.wav (44.1 kHz, stereo).
"""
import wave
import numpy as np

SR = 44100
DUR = 22.0
BEAT = 0.5
N = int(SR * DUR)
rng = np.random.default_rng(7)

L = np.zeros(N)
R = np.zeros(N)
kick_env = np.zeros(N)  # for ducking


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def place(sig, t, gain=1.0, pan=0.0, track=None):
    i = int(round(t * SR))
    if i >= N:
        return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.414
    R[i:i + len(sig)] += sig * gain * r * 1.414
    if track is not None:
        track[i:i + len(sig)] += np.abs(sig) * gain


def env(n, attack=0.002, decay=0.2):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(n, 0.001, 0.16)


def clap():
    n = int(0.25 * SR)
    x = rng.standard_normal(n)
    x = np.diff(x, prepend=0)  # brighten
    e = env(n, 0.001, 0.07) + 0.4 * env(n, 0.012, 0.05)
    return x * e * 0.5


def hat():
    n = int(0.08 * SR)
    x = np.diff(rng.standard_normal(n + 1))
    return x * env(n, 0.0005, 0.018) * 0.5


def tone(freq, dur, kind="tri", attack=0.004, decay=0.25, harmonics=6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "sine":
        s = np.sin(2 * np.pi * freq * t)
    elif kind == "saw":
        s = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, harmonics + 1))
    else:  # triangle-ish
        s = sum(((-1) ** ((k - 1) // 2)) * np.sin(2 * np.pi * freq * k * t) / (k * k) for k in range(1, 9, 2))
    return s * env(n, attack, decay)


def pad(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in notes:
        for det in (-0.12, 0.12):
            s += np.sin(2 * np.pi * midi(m + det) * t)
    a = np.clip(t / 0.35, 0, 1) * np.clip((dur - t) / 0.4, 0, 1)
    return s * a / (2 * len(notes))


def whoosh(dur=0.45):
    n = int(dur * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    y = 0.0
    for i in range(n):
        p = i / n
        a = 0.02 + 0.35 * p * p  # cutoff opens towards the cut
        y += a * (x[i] - y)
        out[i] = y
    shape = np.sin(np.pi * np.clip(np.arange(n) / n, 0, 1)) ** 2
    return out * shape


CHORDS = {
    "C": ([60, 64, 67], 36), "G": ([55, 59, 62], 31), "Am": ([57, 60, 64], 33), "F": ([53, 57, 60], 29),
}
BARS = ["C", "G", "Am", "F", "C", "G", "Am", "F", "C", "G", "C"]

music_duck = np.zeros(N)
padL = np.zeros(N)
padR = np.zeros(N)

for b, name in enumerate(BARS):
    t0 = b * 2.0
    notes, root = CHORDS[name]
    last = b == len(BARS) - 1
    drums = b < len(BARS) - 1  # last bar: drums drop, outro breathes
    # pad (ducked later)
    p = pad(notes + [notes[0] + 12], 2.6 if last else 2.05)
    i = int(t0 * SR)
    seg = p[: N - i]
    padL[i:i + len(seg)] += seg * 0.9
    padR[i:i + len(seg)] += seg * 1.0
    for k in range(4):  # beats
        tb = t0 + k * BEAT
        if drums:
            place(kick(), tb, 0.9 if b > 0 else 0.55, 0.0, track=kick_env)
            if k in (1, 3) and b > 0:
                place(clap(), tb, 0.30, 0.05)
        for h in range(2):  # eighths
            te = tb + h * BEAT / 2
            if drums and h == 1:
                place(hat(), te, 0.11 if b > 0 else 0.06, 0.35)
            if not last or k == 0 and h == 0:
                bass_note = root + (12 if (k == 3 and h == 1) else 0)
                place(tone(midi(bass_note), 0.3, "saw", 0.005, 0.12, harmonics=5), te, 0.30, -0.05)
            # pluck arpeggio on eighths, chord tones up an octave
            if not last:
                seq = [0, 1, 2, 1, 0, 2, 1, 2]
                m = notes[seq[(k * 2 + h) % 8]] + 12
                place(tone(midi(m), 0.4, "tri", 0.003, 0.16), te, 0.14, -0.4 if h == 0 else 0.4)
    if last:  # final chord rings out
        for j, m in enumerate(notes + [notes[0] + 12]):
            place(tone(midi(m + 12), 2.2, "tri", 0.003, 0.9), t0 + j * 0.0625, 0.10, -0.3 + 0.2 * j)

# duck the pad under the kick
duck = np.convolve(kick_env, np.ones(int(0.12 * SR)) / int(0.12 * SR), mode="same")
duck = 1 - 0.45 * np.clip(duck / (duck.max() or 1), 0, 1)
L += padL * 0.16 * duck
R += padR * 0.16 * duck

# ---------------------------------------------------------------- effects ---
PENTA = [72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96, 98]  # C major pentatonic, rising


def tick():
    n = int(0.03 * SR)
    x = np.diff(rng.standard_normal(n + 1))
    return x * env(n, 0.0005, 0.006)


# typing: 16ths while the notes and the install command type
for start, end in ((0.5, 2.5), (19.0, 20.0)):
    t = start
    while t < end - 1e-6:
        place(tick(), t, 0.045, rng.uniform(-0.3, 0.3))
        t += BEAT / 4

# cuts: whoosh rising into each scene change
for cut in (3.0, 7.0, 11.0, 15.0, 18.0):
    w = whoosh(0.45)
    place(w, cut - 0.4, 0.10, 0.0)

# scene 2: bubble lands, lines pop on eighths (C major chord tones)
place(tone(midi(84), 0.4, "sine", 0.002, 0.12), 3.5, 0.10)
for i, m in enumerate([76, 79, 84, 79, 76]):
    place(tone(midi(m), 0.3, "sine", 0.002, 0.08), 3.75 + i * 0.25, 0.06, 0.2)

# scene 3: three soft low "nopes" for the lint errors, then a bright "ready"
for t in (8.0, 8.5, 9.0):
    place(tone(midi(45), 0.35, "tri", 0.004, 0.12), t, 0.16, -0.1)
place(tone(midi(79), 0.5, "sine", 0.002, 0.15), 9.5, 0.08)
for j, m in enumerate((84, 88, 91)):
    place(tone(midi(m), 0.8, "sine", 0.002, 0.3), 10.0 + j * 0.0625, 0.07, 0.15)

# scene 4: card pops on 16ths, rising pentatonic
for i in range(12):
    place(tone(midi(PENTA[i]), 0.25, "sine", 0.001, 0.06), 11.25 + i * 0.125, 0.06, -0.4 + 0.07 * i)

# scene 5: rising tone under the bar fill, landing on the bar line
n = int(1.0 * SR)
tt = np.arange(n) / SR
f = midi(60) * 2 ** (tt / 1.0)
rise = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip(tt / 0.2, 0, 1) * np.clip((1.0 - tt) / 0.1, 0, 1)
place(rise, 15.5, 0.05)
for j, m in enumerate((84, 88, 91, 96)):
    place(tone(midi(m), 0.9, "sine", 0.002, 0.35), 16.5 + j * 0.0625, 0.06)

# scene 6: icon chime
for j, m in enumerate((72, 76, 79, 84)):
    place(tone(midi(m), 1.2, "tri", 0.002, 0.5), 18.0 + j * 0.0625, 0.08, -0.2 + 0.13 * j)

# ------------------------------------------------------------------ master ---
mix = np.stack([L, R], axis=1)
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix /= np.max(np.abs(mix)) / 0.70
fade_in = np.clip(np.arange(N) / (0.01 * SR), 0, 1)
fade_out = np.clip((N - np.arange(N)) / (1.2 * SR), 0, 1)
mix *= (fade_in * fade_out)[:, None]

with wave.open("audio.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("audio.wav", f"{DUR}s", "peak", round(float(np.max(np.abs(mix))), 3))
