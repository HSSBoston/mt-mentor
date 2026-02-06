from music21 import *
import streamlit as st
from PIL import Image
import os, subprocess, shutil
from sight_singing_gen import *

def findMuseScoreCmd():
    for cmd in ("musescore", "mscore", "musescore3"):
        if shutil.which(cmd):
            return cmd
    raise RuntimeError("MuseScore executable not found on PATH.")

MUSESCORE_CMD = findMuseScoreCmd()
# st.write(MUSESCORE_PATH)

if not shutil.which("xvfb-run"):
    raise RuntimeError("xvfb-run not found on PATH.")

env = os.environ.copy()
env["QT_QPA_PLATFORM"] = "offscreen"

def mxml2img():
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, "-r", "300", "melody.xml", "-o", "melody.png"],
        check=True,
        env=env)

def cropHeight():
    img = Image.open("melody-1.png")
    w, h = img.size
    cropped = img.crop((0, 250, w, 700))
    
    if cropped.mode in ("RGBA", "LA"):
        whiteBg = Image.new("RGB", cropped.size, (255, 255, 255))
        whiteBg.paste(cropped, mask=cropped.split()[-1])
        whiteBg.save("melody-1.png")
    else:
        cropped.convert("RGB").save("melody-1.png")
    
def mxml2midi():
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, "melody.xml", "-o", "melody.mid"],
        check=True,
        env=env)

def midi2mp3():
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, "melody.mid", "-o", "melody.wav"],
        check=True,
        env=env)    
    subprocess.run(
        ["ffmpeg", "-y", "-i", "melody.wav", "-codec:a", "libmp3lame", "-q:a", "4", "melody.mp3"],
        check=True)

score = generateSightSingingScore()
score.write("musicxml", "melody.xml")
mxml2img()
cropHeight()
mxml2midi()
midi2mp3()

st.title("Section 2B: Sight-singing")
st.image(Image.open("melody-1.png"))
st.audio("melody.mp3")
