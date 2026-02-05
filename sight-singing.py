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

MUSESCORE_PATH = shutil.which(MUSESCORE_CMD)

if not shutil.which("xvfb-run"):
    raise RuntimeError("xvfb-run not found on PATH.")

env = os.environ.copy()
env["QT_QPA_PLATFORM"] = "offscreen"

def mxml2img(mxmlPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_CMD, mxmlPath, "-o", "melody-image.png"],
        check=True,
        env=env)

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

m21Settings = environment.UserSettings()
m21Settings["musescoreDirectPNGPath"] = MUSESCORE_PATH

score = generateSightSingingScore()
# score.write("musicxml", "melody.xml")
score.write("musicxml.png", fp = "melody-image.png")
score.write("midi",         fp = "melody.mid")

# mxml2img("melody.xml")
# mxml2midi("melody.xml")
midi2mp3("melody.mid")

st.title("Section 2B: Sight-singing")
st.image( Image.open("melody-image-1.png") )
st.audio("melody.mp3")
