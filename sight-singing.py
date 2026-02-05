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

env = os.environ.copy()
env["QT_QPA_PLATFORM"] = "offscreen"

def mxml2img(mxmlPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_PATH, mxmlPath, "-o", "melody-image.png"],
        check=True,
        env=env)

def mxml2midi(mxmlPath):
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_PATH, mxmlPath, "-o", "melody.mid"],
        check=True,
        env=env)

def midi2mp3(midiPath):
#     soundfont = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
#     subprocess.run(
#         ["fluidsynth", "-ni", soundfont, "melody.mid", "-F", "melody.wav", "-r", "44100"],
#         check=True)
    subprocess.run(
        ["xvfb-run", "-a", MUSESCORE_PATH, "melody.mid", "-o", "melody.wav"],
        check=True,
        env=env)    
    subprocess.run(
        ["ffmpeg", "-y", "-i", "melody.wav", "-codec:a", "libmp3lame", "-q:a", "4", "melody.mp3"],
        check=True)

score = generateSightSingingScore()
score.write("musicxml", "melody.xml")
mxml2img("melody.xml")
mxml2midi("melody.xml")
midi2mp3("melody.mid")

st.title("Section 2B: Sight-singing")
st.image( Image.open("melody-image-1.png") )
st.audio("melody.mp3")

st.markdown("aaa <A HREF="melody.mp3">MP3</A>", unsafe_allow_html=True)
