from music21 import *
import streamlit as st
from PIL import Image
import os, subprocess, shutil
from sight_singing_gen import *

def findMusescoreCmd():
    for cmd in ("musescore", "mscore", "musescore3"):
        if shutil.which(cmd):
            return cmd
    raise RuntimeError("MuseScore executable not found on PATH.")

MUSESCORE_CMD = findMusescoreCmd()
# st.write(MUSESCORE_CMD)

if not shutil.which("xvfb-run"):
    raise RuntimeError("xvfb-run not found on PATH.")

def score2imgMidi(score):
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"

#     subprocess.run(
#         ["xvfb-run", "-a", MUSESCORE_APPIMAGE, "-o", "melody-image.png", mxmlPath],
#         check=True,
#         env=env)
    
    m21Settings = environment.UserSettings()
    m21Settings["musescoreDirectPNGPath"] = MUSESCORE_PATH

    score.write("musicxml.png", fp = "melody-image.png")
#     score.write("midi",         fp = "melody.mid")
    

# def score2mp3(score):    
#     cmd = [MUSESCORE_PATH, "melody.mid", "-o", "melody.mp3"]
#     subprocess.run(cmd, check=True)

score = generateSightSingingScore()
score2imgMidi(score)
# score2mp3(score)

st.title("Sight singing question")
st.image( Image.open("melody-image-1.png") )
# st.audio("melody.mp3")
