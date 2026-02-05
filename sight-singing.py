from music21 import *
import streamlit as st
from PIL import Image
import os, subprocess, shutil
from sight_singing_gen import *

def findMuseScorePath():
    for cmd in ("musescore", "mscore", "musescore3"):
        if shutil.which(cmd):
            return cmd
    raise RuntimeError("MuseScore executable not found on PATH.")

MUSESCORE_PATH = findMuseScorePath()
# st.write(MUSESCORE_PATH)

if not shutil.which("xvfb-run"):
    raise RuntimeError("xvfb-run not found on PATH.")

def mxml2imgMidi(mxmlPath):
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"

    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_PATH, "-o", "melody-image.png", mxmlPath],
        check=True,
        env=env)
    
#     score.write("musicxml.png", fp = "melody-image.png")
#     score.write("midi",         fp = "melody.mid")
    

# def score2mp3(score):    
#     cmd = [MUSESCORE_PATH, "melody.mid", "-o", "melody.mp3"]
#     subprocess.run(cmd, check=True)

score = generateSightSingingScore()
score.write("musicxml", "melody.xml")
mxml2imgMidi("melody.xml")
# score2mp3(score)

st.title("Sight singing question")
st.image( Image.open("melody-image.png") )
# st.audio("melody.mp3")
