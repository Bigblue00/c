"""
Record the narration for every episode with an offline neural voice (Kokoro).

    pip install kokoro-onnx soundfile
    # model files from https://github.com/thewh1teagle/kokoro-onnx/releases
    python3 narrate.py --model kokoro-v1.0.int8.onnx --voices voices-v1.0.bin

Writes audio/<episode>/NN.wav and audio/<episode>/durations.json.
Run prepare.py afterwards so the timeline follows the real speech.
"""

import argparse
import json
import os

import soundfile as sf

from episodes import EPISODES, PHASES

HERE = os.path.dirname(os.path.abspath(__file__))

# How some words should be spoken (the subtitles keep the original text).
SAY = {
    "N2O5": "N 2 O 5",
    "Kc": "K c",
    "OIL RIG": "oil rig",
    "2-bromopropane": "two bromo propane",
    "S N 2": "S N two",
    "Delta H": "Delta H",
    "sulphate": "sulfate",
    "sulphuric": "sulfuric",
}


def spoken(text):
    for k, v in SAY.items():
        text = text.replace(k, v)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--voices", required=True)
    ap.add_argument("--voice", default="af_heart")
    ap.add_argument("--speed", type=float, default=0.95)
    ap.add_argument("ids", nargs="*")
    args = ap.parse_args()

    from kokoro_onnx import Kokoro

    tts = Kokoro(args.model, args.voices)
    for ep in EPISODES:
        if args.ids and ep["id"] not in args.ids:
            continue
        folder = os.path.join(HERE, "audio", ep["id"])
        os.makedirs(folder, exist_ok=True)
        durations = []
        n = 0
        for phase in PHASES:
            for line in ep["story"][phase]:
                samples, sr = tts.create(spoken(line), voice=args.voice, speed=args.speed, lang="en-us")
                sf.write(os.path.join(folder, f"{n:02d}.wav"), samples, sr)
                durations.append(len(samples) / sr)
                n += 1
        with open(os.path.join(folder, "durations.json"), "w") as f:
            json.dump(durations, f)
        print(f"{ep['id']:32s} {sum(durations):5.1f} s of speech", flush=True)


if __name__ == "__main__":
    main()
