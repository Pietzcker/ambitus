import copy

# constants for the classic modes
AEOLIAN = 0
LOCRIAN = 1
IONIAN = 2
DORIAN = 3
PHRYGIAN = 4
LYDIAN = 5
MIXOLYDIAN = 6

# number of half tones required to advance one step on the diatonic scale,
# based on A aeolian. This is repeated enough times to span an entire system (21 steps)
steps = (2,1,2,2,1,2,2) * 4

# glyphs for all the clefs
clefs = {"treble": "T", "bass": "B", "alto": "A", "tenor": "t"}

class Note:
    """Builds a Note object that contains information about the base note (CDEFGAB), any alterations (-1 for flat,
    0 for natural, 1 for sharp) and the octave (range 1-6, middle C is C4).
    Note that enharmonically identical notes are not considered equal - E#4 is considered lower than F4
    and E4 is lower than Fb4."""
    def __init__(self, name):
        if 2 > len(name) > 3: 
            raise ValueError(f"Invalid notename: {name}")
        self.note = name[0].upper()
        if not self.note in "ABCDEFG":
            raise ValueError("Key must be one of A, B, C, D, E, F or G (+ optional #/b)!")
        self.noteindex = "CDEFGAB".find(self.note)
        self.alt = 0
        if name[1] == "b":
            self.alt = -1
        elif name[1] == "#":
            self.alt = 1
        elif not name[1] in "123456":
            raise ValueError(f"Not a valid octave: {name[1]}")
        try:
            self.oct = int(name[-1])
        except ValueError:
            print(f"Not a valid octave: {name[-1]}")
            raise
    def __repr__(self):
        match self.alt:
            case -1: 
                acc = "b"
            case 1: 
                acc = "#"
            case 0:
                acc = ""
            case -2: 
                acc = "bb"
            case 2:
                acc = "x"
            case _:
                acc = "ERROR"
        return(f"{self.note}{acc}{self.oct}")
    def __eq__(self, other):
        return (self.oct, self.note, self.alt) == (other.oct, other.note, other.alt)
    def __lt__(self, other):
        return (self.oct, self.noteindex, self.alt) < (other.oct, other.noteindex, other.alt)
    def __le__(self, other):
        return (self.oct, self.noteindex, self.alt) <= (other.oct, other.noteindex, other.alt)
    def __gt__(self, other):
        return (self.oct, self.noteindex, self.alt) > (other.oct, other.noteindex, other.alt)
    def __ge__(self, other):
        return (self.oct, self.noteindex, self.alt) >= (other.oct, other.noteindex, other.alt)
    def __ne__(self, other):
        return (self.oct, self.note, self.alt) != (other.oct, other.note, other.alt)

# legal ranges for all clefs supported by Ambitus, as well as the note on the middle line
ranges = {"bass": {"low": Note("Ab1"), "high": Note("G#4"), "middle": Note("D3")},
          "treble": {"low": Note("Fb3"), "high": Note("E#6"), "middle": Note("B4")},
          "alto": {"low": Note("Gb2"), "high": Note("F#5"), "middle": Note("C4")},
          "tenor": {"low": Note("Eb2"), "high": Note("D#5"), "middle": Note("A3")}
         }


def modal(mode=IONIAN, startkey="C3", stopkey=""):
    """Build a scale using one of the classic modes.
    mode can be set to a value between 0 (AEOLIAN) and 6 (LOCRIAN).
    startkey is composed of a key (one of CDEFGAB), an optional accidental (b or #) and an octave (1-6).
    Note that the lowest possible key in the bass clef is Ab1, and the highest possible key in the
    treble clef is "E#6", so if you exceed these values, you will not be able to build a complete scale.
    Middle C is "C3".
    stopkey is optional. If it is left blank, it will default to one octave above startkey (or "E#6" if lower).
    Return value is a list of notes that can be fed into a glyph generator. Note that it is possible to generate 
    scales that can't be written in Ambitus, e. g. a locrian scale from Cb4 because that would require bb accidentals
    which aren't currently supported in Ambitus."""
    start = Note(startkey)
    if stopkey:
        stop = Note(stopkey)
    else:
        highest = ranges["treble"]["high"] 
        stop = Note(startkey)
        stop.oct +=1
        if stop > highest:
            stop = highest
    if stop < start:
        raise ValueError(f"{stop} is below {start}!")
    current = start
    scale_index = "ABCDEFG".find(start.note)
    mode_index = mode
    notes = []
    while current <= stop:
        notes.append(copy.copy(current))
        basestep = steps[scale_index]
        modestep = steps[mode_index]
        if basestep < modestep:
            current.alt += 1
        elif basestep > modestep:
            current.alt -= 1
        scale_index += 1
        mode_index += 1
        current.note = chr(ord(current.note) + 1)
        current.noteindex = (current.noteindex + 1) % 7
        if current.note == "H":
            current.note = "A"
        elif current.note == "C":
            current.oct += 1
    return notes

def diatonic_distance(note, ref_note):
    return note.noteindex - ref_note.noteindex + 7 * (note.oct - ref_note.oct)

def glyph(note, clef="treble", head="q", stem=""):
    if not ranges[clef]["low"] <= note <= ranges[clef]["high"]:
        print(f'Note {note} out of range for {clef} clef ({ranges[clef]["low"]}-{ranges[clef]["high"]})')
        return None
    distance = diatonic_distance(note, ranges[clef]["middle"])
    match distance:
        case -10:
            distance = "-0"
        case 10:
            distance = "0"
        case 0:
            distance = ""
        case _:
            distance = str(distance)
    match note.alt:
        case -1: 
            acc = "b"
        case 1: 
            acc = "#"
        case 0:
            acc = ""
        case -2: 
            acc = "bb"
        case 2:
            acc = "x"
        case _:
            raise ValueError(f"Invalid accidental value: {note.alt}")
    return f"{acc}{head}{distance}{stem}"

def build_glyphs(notes, clef="treble", head="q", stem=True, sep=":", start="", end=":|"):
    glyphs = []
    for note in notes:
        if g:= glyph(note, clef, head, "" if stem else "s"):
            glyphs.append(g)
    return clefs[clef] + start + sep.join(glyphs) + end

if __name__ == "__main__":
    while True:
        mode = input("Choose mode (first two letters: IO(nian), DO(rian), PH(rygian), LY, MI, AE or LO) or <Enter> to quit: ").upper()
        try:
            mode = ["AE", "LO", "IO", "DO", "PH", "LY", "MI"].index(mode)
        except ValueError:
            print("Exiting...")
            exit()
        while True:
            base = input("Begin scale at (default: C4)? ")
            if not base:
                base = "C4"
            end = input("End scale at or below (default: one octave above the beginning)? ")
            try:
                notes = modal(mode, base, end)
            except ValueError as err:
                print(err)
                continue
            break

        print("Scale: ", notes)
        while True:
            clef = input("Which clef should be used (treble (default), bass, alto or tenor)? ").lower()
            if not clef:
                clef = "treble"
            if clef not in ["treble", "bass", "alto", "tenor"]:
                print("Invalid clef!")
                continue
            break
        while True:
            sep = input("Choose separator (one of ;:/?_ (default ':')): ")
            if not sep:
                sep = ":"
            if sep not in [";", ":", "/", "?", "_"]:
                print("Invalid separator!")
                continue
            break
        while True:
            head = input("Choose notehead (one of q (default), h, w): ").lower()
            if not head:
                head = "q"
            if head not in ["q", "h", "w"]:
                print("Invalid notehead!")
                continue
            break
        stem = True
        if head in "qh":
            stem = input("Remove stems (default: No)? ")
            if stem:
                if stem[0].lower() == "y":
                    stem = False 
        start = input("Any additional spacing in front of the scale (one of ;:/?_ or leave blank)? ")
        end = input("Any additional characters at the end (default ':|')? ")
        if not end:
            end = ":|"

        print()
        print(build_glyphs(notes, clef, head, stem, sep, start, end))
        print()



