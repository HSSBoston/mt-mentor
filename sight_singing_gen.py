from music21 import *
import random, numpy as np

RANDOM_SEED_NOTE = None #None or int
rng = np.random.default_rng(seed=RANDOM_SEED_NOTE)

# Pitch-to-pitch transition matrix
# P = np.array([
#     [0,   0.4,  0.4, 0.2,  0,   0,    0,    0],
#     [0.3, 0,    0.4, 0.3,  0,   0,    0,    0],
#     [0.1, 0.4,  0,   0.4,  0.1, 0,    0,    0],
#     [0,   0.15, 0.4, 0,    0.4, 0.05, 0,    0],
#     [0,   0,    0.2, 0.65, 0,   0.1,  0.05, 0],
#     [0,   0,    0,   0.3,  0.5, 0,    0.2,  0],
#     [0,   0,    0,   0.1,  0.1, 0.3,  0,    0.5],
#     [0,   0,    0,   0,    0.6, 0,    0.4,  0]])
P = np.array([
    [0,   0.5,  0.45, 0.05, 0,    0,    0,    0],
    [0.3, 0,    0.55, 0.1,  0.05, 0,    0,    0],
    [0.1, 0.4,  0,    0.4,  0.1,  0,    0,    0],
    [0,   0.15, 0.4,  0,    0.4,  0.05, 0,    0],
    [0,   0.01, 0.2,  0.39, 0,    0.35, 0.05, 0],
    [0,   0,    0,    0.05, 0.65, 0,    0.3,  0],
    [0,   0,    0,    0,    0.01, 0.34, 0,    0.65],
    [0,   0,    0,    0,    0.4,  0.3,  0.3,  0]])

# Rhythm patterns for the 1st measure in 4/4 (FF) time
measureOneFF = [
    [1, 1,   0.5, 0.5, 1],
    [1, 1,   1,   0.5, 0.5],
    [1, 0.5, 0.5, 1,   1],
    [1, 1,   1,   1],
    [1, 1,   0.5, 0.5, 0.5, 0.5],
    [1, 0.5, 0.5, 0.5, 0.5, 1]]

# Rhythm patterns for the 2nd measure in 4/4 (FF) time
measureTwoFF = [
    [0.5, 0.5, 1,   1.5, 0.5],
    [1.5, 0.5, 2],
    [1,   1,   1.5, 0.5],
    [1,   1.5, 0.5, 1],
    [1,   0.5, 0.5, 0.5, 0.5, 1],
    [0.5, 0.5, 0.5, 0.5, 1,   1],
    [0.5, 0.5, 0.5, 0.5, 1.5, 0.5],
    [0.5, 0.5, 1,   1.5, 0.5],
    [1,   0.5, 0.5, 1.5, 0.5],
    [0.5, 0.5, 1,   1,   1]]

# Rhythm patterns for the 3rd measure in 4/4 (FF) time
measureThreeFF = [
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

# Rhythm patterns for the 4th measure in 4/4 (FF) time
measureFourFF = [
    [1,   1,   2],
    [0.5, 0.5, 1,   2],
    [1,   0.5, 0.5, 2]]

# Rhythm patterns for the 1st measure in 6/8 (SE) time
measureOneSE = [
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5, 1,   0.5],
    [0.5, 0.5, 0.5, 0.5, 1],
    [1,   0.5, 0.5, 0.5, 0.5],
    [0.5, 1,   0.5, 0.5, 0.5],
    [1,   0.5, 1,   0.5],
    [0.5, 1,   0.5, 1],
    [1,   0.5, 0.5, 1]]

# Rhythm patterns for the 2nd measure in 6/8 (SE) time
measureTwoSE = [
    [0.75, 0.25, 0.5,  1,    0.5],
    [0.75, 0.25, 0.5,  1.5],
    [0.75, 0.25, 0.5,  0.5,  1],
    [0.5,  0.5,  0.5,  1,    0.5],
    [0.5,  0.5,  0.5,  0.5,  1],
    [0.5, 0.5, 0.5,  1.5]]

# Rhythm patterns for the 3rd measure in 6/8 (SE) time
measureThreeSE = [
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

# Rhythm patterns for the 4th measure in 6/8 (SE) time
measureFourSE = [
    [0.5, 0.5, 0.5, 1.5],
    [1,   0.5, 1.5],
    [0.5, 1,   1.5]]

# Key choices
keyLettersList = ["C","G","D","F","B-","E-",
                  "a","e","b", "d", "g", "c"]

# adjust the octave of a new note by prioritizing stepwise melodic motion
def adjustOctave(newNote, prevNote):
    if (newNote.pitch.midi - prevNote.pitch.midi) >= 7:
        newNote.octave -= 1
        print("Octave adjustment:", newNote.octave+1, "->", newNote.octave, end="")
        return True
    elif (prevNote.pitch.midi - newNote.pitch.midi) >= 7:
        newNote.octave += 1
        print("Octave adjustment:", newNote.octave-1, "->", newNote.octave, end="")
        return True
    else:
        return False

def note2NoteSD(noteObj, scalePitchNames) -> int:
    return scalePitchNames.index(noteObj.nameWithOctave) + 1

def transition(prevNoteObj, scalePitchNames) -> int:
    newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                           p=P[scalePitchNames.index(prevNoteObj.nameWithOctave)])
    return newNoteSD

def getWeightedProbDist(probDist, weightVector):
    weightedProbDist = probDist * weightVector # element-wise multiplication
    total = np.sum(weightedProbDist, dtype=float)
    return weightedProbDist / total

def cadentialPrepTransition(prevNoteObj, scalePitchNames) -> int:
    weightedP = getWeightedProbDist(
        P[scalePitchNames.index(prevNoteObj.nameWithOctave)],
        [0, 3, 0, 0, 3, 0, 0, 0])
    newNoteSD = rng.choice(["1", "2", "3", "4", "5", "6", "7", "8"],
                           p=weightedP)
    return newNoteSD


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
        if keyLetter in ["G", "F", "B-", "a", "b", "g"]:
            for p in sc.getPitches(keyLetter+"2"):
                scalePitchNames.append(p.nameWithOctave)
        else:
            for p in sc.getPitches(keyLetter+"3"):
                scalePitchNames.append(p.nameWithOctave)            
    print("Clef:", cl)
    print("Scale pitch names", scalePitchNames)

    # Time signature selection
    timeSig = random.choice(["4/4", "6/8"])
    print("Time signature:", timeSig)

    # Score initialization
    score = stream.Score()
    melody = stream.Part()
    m1 = stream.Measure()
    m1.append(cl)
    m1.insert(0, meter.TimeSignature(timeSig))
    m1.keySignature = k
    m1.insert(0, tempo.MetronomeMark("Adagio", 60))
    m2 = stream.Measure()
    m3 = stream.Measure()
    m4 = stream.Measure()
    m4.rightBarLine = bar.Barline("final")

    if timeSig == "4/4":
        m1Rhythm = random.choice(measureOneFF)
        m2Rhythm = random.choice(measureTwoFF)
        m3Rhythm = random.choice(measureThreeFF)
        m4Rhythm = random.choice(measureFourFF)
    else:
        m1Rhythm = random.choice(measureOneSE)
        m2Rhythm = random.choice(measureTwoSE)
        m3Rhythm = random.choice(measureThreeSE)
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
            newNote = note.Note(scalePitchNames[0])
            newNote.quarterLength = noteDuration
            if cl == clef.BassClef():
                if scalePitchNames[0][-1] == "2":
#                 if keyLetter in ["G", "F", "B-", "a", "b", "g"]:
                    newNote.octave = 2
                else:
                    newNote.octave = 3
            else:
                newNote.octave = 4
        else:
            newNoteSD = transition(prevNote, scalePitchNames)
            newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
            newNote.quarterLength = noteDuration
            newNote.octave = m1.notes.first().octave        

            if adjustOctave(newNote, prevNote):
                print(" Measure 1, Note index", index)
        prevNote = newNote
        m1.append(newNote)

    # MEASURE 2
    #
    # If the last note in the measure has a long duration (>0.5),
    # end a half cadence with the note.
    if m2Rhythm[-1] > 0.5:
        halfCadentialPointIndex = len(m2Rhythm) - 1
    # If the last note in the measure has a short duration (<=0.5) and
    # the second note from the end of the measure has a long duration (>0.5),
    # end a half cadence with the second note from the end.
    elif m2Rhythm[-2] > 0.5:
        halfCadentialPointIndex = len(m2Rhythm) - 2
        
    for index, noteDuration in enumerate(m2Rhythm):
        prevNoteSD = note2NoteSD(prevNote, scalePitchNames)
        # If in the cadence-ending point
        if index == halfCadentialPointIndex:
            if prevNoteSD == 2:
                newNoteSD = 5
            elif prevNoteSD == 5:
                newNoteSD = 2
            else:
                if abs(prevNoteSD - 5) <= abs(prevNoteSD - 2):
                    newNoteSD = 5
                else:
                    newNoteSD = 2                
#                 newNoteSD = random.choice([2, 5])        
        # If the note after the cadence-ending point
        elif index == halfCadentialPointIndex + 1:
            if prevNoteSD == 5:
                newNoteSD = random.choice([5, 6, 7, 8])
            elif prevNoteSD == 2:
                newNoteSD = random.choice([3, 4])
        else:
            newNoteSD = transition(prevNote, scalePitchNames)
            
        newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
        newNote.quarterLength = noteDuration
        newNote.octave = m1.notes.first().octave
        
        if adjustOctave(newNote, prevNote):
            print(" Measure 2, Note index", index)
        
        print("Measure 2, Note index", index, ", SD", newNoteSD)
        prevNote = newNote
        m2.append(newNote)
    
    sl1 = spanner.Slur([m1.notes[0], m2.notes[halfCadentialPointIndex]])
    m2.insert(0, sl1)
        
    # MEASURE 3
    for index, noteDuration in enumerate(m3Rhythm):
        # If the last note in measure 2 is scale degree 5
        # the first note should be scale degree 5, 6, 7, or 8.
        if index == 0 and note2NoteSD(m2.notes.last(), scalePitchNames) == 5:
                newNoteSD = random.choice([5, 6, 7, 8])
        # If the last note in measure 2 is scale degree 2
        # the first note shoujld be scale degree 3 or 4. 
        elif index == 0 and note2NoteSD(m2.notes.last(), scalePitchNames) == 2:
                newNoteSD = random.choice([3, 4])
        else:
            newNoteSD = transition(prevNote, scalePitchNames)

        newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
        newNote.quarterLength = noteDuration
        newNote.octave = m1.notes.first().octave
        
        if adjustOctave(newNote, prevNote):
            print(" Measure 3, Note index", index)
        prevNote = newNote
        m3.append(newNote)

    # Measure 4
    for index, noteDuration in enumerate(m4Rhythm):
        # if the last note in the measure
        if index == len(m4Rhythm) - 1: 
            newNote = note.Note(scalePitchNames[0])
            if cl == clef.BassClef():
                if scalePitchNames[0][-1] == "2":
#                 if keyLetter in ["G", "F", "B-", "a", "b", "g"]:
                    newNote.octave = 2
                else:
                    newNote.octave = 3
            else:
                newNote.octave = 4
            newNote.quarterLength = noteDuration
        else:
            # if the second note from the end of the measure
            if index == len(m4Rhythm) - 2:
                prevNoteSD = note2NoteSD(prevNote, scalePitchNames)
                if prevNoteSD == 4:
                    newNoteSD = random.choice([5,2])
                    print("!!!", prevNoteSD, newNoteSD)                    
                else:
                    newNoteSD = cadentialPrepTransition(prevNote, scalePitchNames)
            else:
                newNoteSD = transition(prevNote, scalePitchNames)
            
            print("Measure 4, Note index", index, ", SD", newNoteSD)
            newNote = note.Note(scalePitchNames[int(newNoteSD)-1])
            newNote.quarterLength = noteDuration
            newNote.octave = m1.notes.first().octave
            
            if adjustOctave(newNote, prevNote):
                print(" Measure 4, Note index", index)
        prevNote = newNote
        m4.append(newNote)
        
    if halfCadentialPointIndex == len(m2Rhythm)-1:
        sl2 = spanner.Slur([m3.notes[0],m4.notes[-1]])
    else:
        sl2 = spanner.Slur([m2.notes[halfCadentialPointIndex+1], m4.notes[-1]])
    
    m4.insert(sl2)
    
    
    melody.append(m1)
    melody.append(m2)
    melody.append(m3)
    melody.append(m4)
    score.insert(0, melody)
    score.insert(0, metadata.Metadata())
    score.metadata.title = ""
    score.metadata.composer = "The Music Theory Mentor"
    return score

if __name__ == "__main__":
    score = generateSightSingingScore()
#     score.show("text")
    score.show()
