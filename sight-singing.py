from music21 import *
import streamlit as st
from PIL import Image, ImageChops
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

def mxml2img(mxmlPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, mxmlPath, "-o", "melody-image.png"],
        check=True,
        env=env)

def verticalAutoCrop(bg_color=(255, 255, 255)):
    img = Image.open("melody-1.png").convert("RGB")
    # Create background image
    bg = Image.new("RGB", img.size, bg_color)
    # Difference between image and background
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        img.crop(bbox).save("melody-1.png")
    else:
        img.save("melody-1.png")

def mxml2midi(mxmlPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, mxmlPath, "-o", "melody.mid"],
        check=True,
        env=env)

def midi2mp3(midiPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, "melody.mid", "-o", "melody.wav"],
        check=True,
        env=env)    
    subprocess.run(
        ["ffmpeg", "-y", "-i", "melody.wav", "-codec:a", "libmp3lame", "-q:a", "4", "melody.mp3"],
        check=True)

score = generateSightSingingScore()
score.write("musicxml", "melody.xml")
verticalAutoCrop()
mxml2img("melody.xml")
mxml2midi("melody.xml")
midi2mp3("melody.mid")

st.title("Section 2B: Sight-singing")
st.image( Image.open("melody-image-1.png") )
st.audio("melody.mp3")
