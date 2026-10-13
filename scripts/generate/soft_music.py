"""Generate a soft, cheerful, non-spooky instrumental bed using only the Python standard library.

A gentle C-major/pentatonic bell melody with warm sustained chords; no sudden stingers,
minor-key suspense, harsh noise, or loud effects. This is intentionally royalty-free
procedural audio created for the HAPPY HIPPO channel.
"""
from __future__ import annotations

import argparse
import math
import struct
import wave
from pathlib import Path

RATE = 22050

def envelope(t: float, length: float) -> float:
    attack = min(1.0, t / 0.035)
    release = min(1.0, max(0.0, (length - t) / 0.16))
    return attack * release

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    duration = max(20.0, min(60.0, args.duration))
    total = int(RATE * duration)
    # C-major pentatonic notes, chosen to feel playful and comforting.
    melody = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.00, 698.46,
              523.25, 587.33, 659.25, 783.99, 698.46, 587.33, 523.25, 392.00]
    beat = 0.52
    # Gentle consonant triads, changing slowly under the melody.
    chords = [
        (130.81, 164.81, 196.00),  # C
        (174.61, 220.00, 261.63),  # F
        (146.83, 196.00, 220.00),  # G
        (130.81, 164.81, 196.00),  # C
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        block = bytearray()
        for i in range(total):
            t = i / RATE
            note_index = int(t / beat) % len(melody)
            note_t = t % beat
            note_len = beat * 0.86
            bell_env = envelope(note_t, note_len)
            f = melody[note_index]
            bell = (math.sin(2 * math.pi * f * t)
                    + 0.22 * math.sin(2 * math.pi * f * 2 * t)
                    + 0.08 * math.sin(2 * math.pi * f * 3 * t)) * bell_env * 0.105
            chord = chords[int(t / 2.08) % len(chords)]
            pad = sum(math.sin(2 * math.pi * cf * t) for cf in chord) / 3
            pad += 0.22 * math.sin(2 * math.pi * (chord[0] / 2) * t)
            # Slow breathing swell avoids abrupt changes.
            swell = 0.72 + 0.18 * math.sin(2 * math.pi * t / 7.5)
            sample = (bell + pad * 0.045 * swell) * 0.72
            # Gentle fade at both ends.
            fade_in = min(1.0, t / 1.0)
            fade_out = min(1.0, max(0.0, (duration - t) / 1.5))
            sample *= fade_in * fade_out
            value = max(-1.0, min(1.0, sample))
            block.extend(struct.pack("<h", int(value * 32767)))
            if len(block) >= 65536:
                out.writeframesraw(block)
                block.clear()
        if block:
            out.writeframesraw(block)
    print(f"SOFT_MUSIC_READY duration={duration:.2f}s rate={RATE}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
