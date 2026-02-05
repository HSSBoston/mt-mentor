from music21 import *
import random, numpy as np

RANDOM_SEED_NOTE = None #None or int
rng = np.random.default_rng(seed=RANDOM_SEED_NOTE)

# Pitch-to-pitch transition matrix
P = np.array([
    [0,   0.4,  0.4, 0.2,  0,   0,    0,    0],
    [0.3, 0,    0.4, 0.3,  0,   0,    0,    0],
    [0.1, 0.4,  0,   0.4,  0.1, 0,    0,    0],
    [0,   0.15, 0.4, 0,    0.4, 0.05, 0,    0],
    [0,   0,    0.2, 0.65, 0,   0.1,  0.05, 0],
    [0,   0,    0,   0.3,  0.5, 0,    0.2,  0],
    [0,   0,    0,   0.1,  0.1, 0.3,  0,    0.5],
    [0,   0,    0,   0,    0.6, 0,    0.4,  0]])

# Rhythm patterns for the 1st measure when in 4/4 (FF) time
measureOneFF = [
    [1, 1,   0.5, 0.5, 1],
    [1, 1,   1,   0.5, 0.5],
    [1, 0.5, 0.5, 1,   1],
    [1, 1,   1,   1],
    [1, 1,   0.5, 0.5, 0.5, 0.5],
    [1, 0.5, 0.5, 0.5, 0.5, 1]]

# Rhythm patterns for the 2nd and 3rd measures when in 4/4 (FF) time
measureTwoThreeFF = [
    [0.5, 0.5, 1,   1.5, 0.5],
    [1.5, 0.5, 2],
    [1.5, 0.5, 1,   0.5, 0.5],
    [1,   1,   1.5, 0.5],
    [0.5, 0.5, 0.5, 0.5, 1.5, 0.5],
    [1,   1.5, 0.5, 1],
    [1,   1,   0.5, 0.5, 0.5, 0.5],
    [1,   0.5, 0.5, 0.5, 0.5, 1],
    [1,   1,   0.5, 0.5, 0.5, 0.5],
    [0.5, 0.5, 1,   1,   0.5, 0.5],
    [0.5, 0.5, 0.5, 0.5, 1,   1]]

# Rhythm patterns for the 4th measure when in 4/4 (FF) time
measureFourFF = [
    [1,   1,   2],
    [0.5, 0.5, 1,   2],
    [1,   0.5, 0.5, 2]]

# Rhythm patterns for the 1st measure when in 6/8 (SE) time
measureOneSE = [
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5, 1,   0.5],
    [0.5, 0.5, 0.5, 0.5, 1],
    [1,   0.5, 0.5, 0.5, 0.5],
    [0.5, 1,   0.5, 0.5, 0.5],
    [1,   0.5, 1,   0.5],
    [0.5, 1,   0.5, 1],
    [1,   0.5, 0.5, 1]]

# Rhythm patterns for the 2nd and 3rd measures when in 6/8 (SE) time
measureTwoThreeSE = [
    [0.75, 0.25, 0.5,  0.5,  0.5,  0.5],
    [0.75, 0.25, 0.5,  1,    0.5],
    [0.75, 0.25, 0.5,  0.5,  1],
    [0.5,  0.5,  0.5,  0.75, 0.25, 0.5],
    [0.5,  1,    0.75, 0.25, 0.5],
    [1,    0.5,  0.75, 0.25, 0.5],
    [0.5,  0.5,  0.5,  1,    0.5],
    [0.5,  0.5,  0.5,  0.5,  1],
    [1,    0.5,  0.5,  0.5,  0.5],
    [0.5,  1,    0.5,  0.5,  0.5],
    [1,    0.5,  1,    0.5],
    [0.5,  1,    0.5,  1],
    [1,    0.5,  0.5,  1]]

# Rhythm patterns for the 4th measure when in 6/8 (SE) time
measureFourSE = [
    [0.5, 0.5, 0.5, 1.5],
    [1,   0.5, 1.5],
    [0.5, 1,   1.5]]

# Key choices
keyLettersList = ["C","G","D","A","F","B-","E-",
                  "a","e","b", "d", "g", "c"]

# adjust the octave of a new note by prioritizing stepwise melodic motion
def adjustOctave(newNote, prevNote):
    if (newNote.pitch.midi - prevNote.pitch.midi) >= 7:
        newNote.octave -= 1
        print("Octave adjustment. SD", newNote.octave+1, "-> SD", newNote.octave, end="")
        return True
    elif (prevNote.pitch.midi - newNote.pitch.midi) >= 7:
        newNote.octave += 1
        print("Octave adjustment. SD", newNote.octave-1, "-> SD", newNote.octave, end="")
        return True
    else:
        return False

def generateSightSingingScore():
    # Key selection
    keyLetter = random.choice(keyLettersList)
    k = key.Key(keyLetter)
    print("Key:", k)

    if k.mode == "major":
      sc = scale.MajorScale(keyLetter)
    else:
      sc = scale.HarmonicMinorScale(keyLetter)

    # Clef selection
    scalePitchNames = [] # Pitch names with an octave number ("C4") in the selected key

    randomFloat = random.random()
    if randomFloat < 0.5:
        cl = clef.TrebleClef()
        for p in sc.getPitches(keyLetter+"4"):
            scalePitchNames.append(p.nameWithOctave)
    else:
        cl = clef.BassClef()
        for p in sc.getPitches(keyLetter+"3"):
            scalePitchNames.append(p.nameWithOctave)
    print("Clef:",    cl)
    print("Scale pitch names", scalePitchNames)

    # Time signature selection
    randomFloat = random.random()
    if randomFloat < 0.5:
        timeSig = "4/4"
    else:
        timeSig = "6/8"
    print("Time signature:", timeSig)

    # Score initialization
    melody = stream.Part()
    m1 = stream.Measure()
    m1.append(cl)
    m1.insert(0, meter.TimeSignature(timeSig))
    m1.keySignature = k
    m2 = stream.Measure()
    m3 = stream.Measure()
    m4 = stream.Measure()
    m4.rightBarLine = bar.Barline("final")

    if timeSig == "4/4":
        m1Rhythm = random.choice(measureOneFF)
        m2Rhythm = random.choice(measureTwoThreeFF)
        m3Rhythm = random.choice(measureTwoThreeFF)
        m4Rhythm = random.choice(measureFourFF)
    else:
        m1Rhythm = random.choice(measureOneSE)
        m2Rhythm = random.choice(measureTwoThreeSE)
        m3Rhythm = random.choice(measureTwoThreeSE)
        m4Rhythm = random.choice(measureFourSE)
    print("Rhythm pattern for measure 1:", m1Rhythm)
    print("Rhythm pattern for measure 2:", m2Rhythm)
    print("Rhythm pattern for measure 3:", m3Rhythm)
    print("Rhythm pattern for measure 4:", m4Rhythm)

    prevNote = None

    # Melody generation
    # Measure 1
    for index, noteDuration in enumerate(m1Rhythm):
        if index == 0:
            newNote = note.Note(k.tonic)
            newNote.quarterLength = noteDuration
            if cl == clef.BassClef():
                newNote.octave = 3
            else:
                newNote.octave = 4
        else:
            newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                                   p=P[scalePitchNames.index(prevNote.nameWithOctave)])
            newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
            newNote.quarterLength = noteDuration
            newNote.octave = m1.notes.first().octave        

            if adjustOctave(newNote, prevNote):
                print(" Measure 1, Note index", index)
        prevNote = newNote
        m1.append(newNote)

    # Measure 2
    for index, noteDuration in enumerate(m2Rhythm):
        newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                               p=P[scalePitchNames.index(prevNote.nameWithOctave)])
        newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
        newNote.quarterLength = noteDuration
        newNote.octave = m1.notes.first().octave
        
        if adjustOctave(newNote, prevNote):
            print(" Measure 2, Note index", index)
        prevNote = newNote
        m2.append(newNote)
        
    # Measure 3
    for index, noteDuration in enumerate(m3Rhythm):
        newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                               p=P[scalePitchNames.index(prevNote.nameWithOctave)])
        newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
        newNote.quarterLength = noteDuration
        newNote.octave = m1.notes.first().octave
        
        if adjustOctave(newNote, prevNote):
            print(" Measure 3, Note index", index)
        prevNote = newNote
        m3.append(newNote)

    # Measure 4
    for index, noteDuration in enumerate(m4Rhythm):
        if index == len(m4Rhythm) - 1:
            newNote = note.Note(k.tonic)
            if cl == clef.BassClef():
                newNote.octave = 3
            else:
                newNote.octave = 4
            newNote.quarterLength = noteDuration
        else:
            newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                                   p=P[scalePitchNames.index(prevNote.nameWithOctave)])
            newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
            newNote.quarterLength = noteDuration
            newNote.octave = m1.notes.first().octave
            
            if adjustOctave(newNote, prevNote):
                print(" Measure 4, Note index", index)
        prevNote = newNote
        m4.append(newNote)

    melody.append(m1)
    melody.append(m2)
    melody.append(m3)
    melody.append(m4)
    return melody

if __name__ == "__main__":
    score = generateSightSingingScore()
    score.show("text")
#     score.show()
