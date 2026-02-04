from music21 import *
import random, numpy as np
# from midi2audio import FluidSynth
import os
import streamlit as st
from PIL import Image
import subprocess
# from pydub import AudioSegment

m21Settings = environment.UserSettings()
m21Settings["musescoreDirectPNGPath"] = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
print( m21Settings["musescoreDirectPNGPath"] )

RANDOM_SEED_NOTE = None #None or int
rng = np.random.default_rng(seed=RANDOM_SEED_NOTE)

P = np.array(
    [[0, 0.4, 0.4, 0.1, 0.1, 0, 0, 0],
     [0.3, 0, 0.4, 0.3, 0, 0, 0, 0],
     [0.1, 0.4, 0, 0.4, 0.1, 0, 0, 0],
     [0, 0.1, 0.4, 0, 0.4, 0.1, 0, 0],
     [0, 0, 0.2, 0.6, 0, 0.1, 0.05, 0.05],
     [0, 0, 0, 0.3, 0.5, 0, 0.2, 0],
     [0, 0, 0, 0.1, 0.1, 0.3, 0, 0.5],
     [0, 0, 0, 0, 0, 0.5, 0.5, 0]
     ])

measureOneFF = [" T4 4 8 8 4 ",
                " T4 4 4 8 8 ",
                " T4 8 8 4 4 ",
                " T4 4 4 4 ",
                " T4 4 8 8 8 8 ",
                " T4 8 8 8 8 4 "]

measureTwoThreeFF = [" 8 8 4 4. 8 ",
                    " 4. 8 2 ",
                    " 4. 8 4 8 8 ",
                    " 4 4 4. 8 ",
                    " 8 8 8 8 4. 8 ",
                    " 4 4. 8 4 ",
                    " 4 4 8 8 8 8 ",
                    " 4 8 8 8 8 4 ",
                    " 4 4 8 8 8 8 ",
                    " 8 8 4 4 8 8 ",
                    " 8 8 8 8 4 4 "]

measureFourFF = [" 4 4 T2 ",
                " 8 8 4 T2 ",
                " 4 8 8 T2 "]

#up to four accidentals only (to keep problems not too hard)
keysLettersList = ["C","G","D","A","E","F","B-","E-","A-","a","e","b","f#", "d", "g", "c","f"]
keyLetter = random.choice(keysLettersList)
k = key.Key(keyLetter)

if k.mode == "major":
  sc = scale.MajorScale(keyLetter)
else:
  sc = scale.MinorScale(keyLetter)

scalePitchNames = []
scaleMidi = []

for p in sc.getPitches():
  scalePitchNames.append(p.name)
  scaleMidi.append(p.midi)      

#randomInt = random.randint(0,1)
#
# if randomInt < 0.5:
#     timeSig == "4/4"
# else:
#     timeSig == "6/8"

randomInt = random.randint(0,1)
if randomInt < 0.5:
    cl = clef.TrebleClef()
else:
    cl = clef.BassClef()

cl = clef.TrebleClef()
timeSig = "4/4"

if timeSig == "4/4":
        
    rhythmString = random.choice(measureOneFF)+random.choice(measureTwoThreeFF)+random.choice(measureTwoThreeFF)+random.choice(measureFourFF)
    print(rhythmString)
    melodyString = "tinyNotation: 4/4"  
    for num in rhythmString.split():
        if "T" in num:
            newNote = note.Note(k.tonic)
            num = num[-1]
            newNoteSD = "1"
            noteName = newNote.name.lower()
        else:
            newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"], p=P[scalePitchNames.index(temp.name)])
            newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
            
            if newNote.name == k.getLeadingTone().name and keyLetter.islower():
                newNote.pitch.accidental("sharp")
                
            if cl == clef.TrebleClef():
                s = converter.parse("tinyNotation: " + newNote.name.lower() + tempNoteString)

                if abs(s.recurse().notes.first().pitch.midi - s.flatten().notes[1].pitch.midi) > 7:
                    if len(newNote.name) > 1:
                        noteName = newNote.name[0].lower() + "'"
                    else:
                        noteName = newNote.name[0].lower() + "'" + newNote.name[1:]
                else:
                    noteName = newNote.name.lower()
            else:
                s = converter.parse("tinyNotation: " + newNote.name.upper() + tempNoteString)
                
                if abs(s.recurse().notes.first().pitch.midi - s.flatten().notes[1].pitch.midi) > 5:
                    noteName = newNote.name.lower()
                else:
                    noteName = newNote.name.upper()
            
        noteString = " " + noteName + num + " "
        melodyString += noteString
        temp = newNote
        tempNoteString = noteString
    

melody = converter.parse(melodyString)
melody.measure(1).keySignature = key.Key(keyLetter)
# if cl == clef.BassClef:
#     melody.measure(1).clef = cl
melody.insert(0.0, tempo.MetronomeMark(60))
#melody.show()

melody.write("musicxml.png", fp = "melody-image.png")
midiFile= melody.write("midi", fp = "melody.mid")

museScoreCmd = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
cmd = [museScoreCmd, "melody.mid", "-o", "melody.mp3"]
subprocess.run(cmd, check=True)

st.title("Sight singing")
st.image( Image.open("melody-image-1.png") )
st.audio("melody.mp3")
