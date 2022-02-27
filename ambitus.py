import copy

# number of half tones required to advance one step on the diatonic scale,
# based on A aeolian.
steps = (2,1,2,2,1,2,2) 

scales = {"Major":          (2,2,1,2,2,2,1),
          "Natural minor":  (2,1,2,2,1,2,2),
          "Harmonic minor": (2,1,2,2,1,3,1),
          "Aeolian":    (2,1,2,2,1,2,2),
          "Locrian":    (1,2,2,1,2,2,2),
          "Ionian":     (2,2,1,2,2,2,1),
          "Lydian":     (2,2,2,1,2,2,1),
          "Dorian":     (2,1,2,2,2,1,2),
          "Phrygian":   (1,2,2,2,1,2,2),
          "Mixolydian": (2,2,1,2,2,1,2),
          "Melodic minor":    (2,1,2,2,2,2,1),
          "Phrygian n6":      (1,2,2,2,2,1,2),
          "Lydian augmented": (2,2,2,2,1,2,1),
          "Lydian dominant":  (2,2,2,1,2,1,2),
          "Mixolydian b6":    (2,2,1,2,1,2,2),
          "Locrian n2":       (2,1,2,1,2,2,2),
          "Altered dominant": (1,2,1,2,2,2,2),
          }

signatures = {"c":   [0],
              "am":  [0],
              "f":   [-1, "B"],
              "dm":  [-1, "B"],
              "bb":  [-1, "B", "E"],
              "gm":  [-1, "B", "E"],
              "eb":  [-1, "B", "E", "A"],
              "cm":  [-1, "B", "E", "A"],
              "ab":  [-1, "B", "E", "A", "D"],
              "fm":  [-1, "B", "E", "A", "D"],
              "db":  [-1, "B", "E", "A", "D", "G"],
              "bbm": [-1, "B", "E", "A", "D", "G"],
              "gb":  [-1, "B", "E", "A", "D", "G", "C"],
              "ebm": [-1, "B", "E", "A", "D", "G", "C"],
              "cb":  [-1, "B", "E", "A", "D", "G", "C", "F"],
              "abm": [-1, "B", "E", "A", "D", "G", "C", "F"],
              "g":   [1, "F"],
              "em":  [1, "F"],
              "d":   [1, "F", "C"],
              "bm":  [1, "F", "C"],
              "a":   [1, "F", "C", "G"],
              "f#m": [1, "F", "C", "G"],
              "e":   [1, "F", "C", "G", "D"],
              "c#m": [1, "F", "C", "G", "D"],
              "b":   [1, "F", "C", "G", "D", "A"],
              "g#m": [1, "F", "C", "G", "D", "A"],
              "f#":  [1, "F", "C", "G", "D", "A", "E"],
              "d#m": [1, "F", "C", "G", "D", "A", "E"],
              "c#":  [1, "F", "C", "G", "D", "A", "E", "B"],
              "a#m": [1, "F", "C", "G", "D", "A", "E", "B"]
             }

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



def diatonic(scale="Major", startkey="C4", stopkey=""):
    """Build a diatonic scale .
    startkey is composed of a key (one of CDEFGAB), an optional accidental (b or #) and an octave (1-6).
    Note that the lowest possible key in the bass clef is Ab1, and the highest possible key in the
    treble clef is "E#6", so if you exceed these values, you will not be able to build a complete scale.
    Middle C is "C3".
    stopkey is optional. If it is left blank, it will default to one octave above startkey (or "E#6" if lower).
    Return value is a list of notes that can be fed into a glyph generator. Note that it is possible to generate 
    scales that can't be written in Ambitus."""

    try:
        scale = scales[scale]
    except KeyError:
        print(f"Unknown scale {scale}! Choose one of the following:")
        for scale in scales.keys():
            print(scale)
        exit()

    # Convert start and stop key into valid Note objects
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

    # Step through the scale from the chosen starting note
    current = start
    base_index = "ABCDEFG".find(start.note)  # Use the aeolian scale as reference
    scale_index = 0                          # Mark the position within the chosen scale
    notes = []
    while current <= stop:
        notes.append(copy.copy(current))
        basestep = steps[base_index]         # How many halftone steps would it take on the basic scale,...
        scalestep = scale[scale_index]       # ... and how many on the chosen scale to advance to the next note?
        current.alt += scalestep-basestep    # If they differ, the number of accidentals must increase or decrease
        base_index = (base_index + 1) % 7    # Advance one note, wrapping around after 7 steps
        scale_index = (scale_index + 1) % 7  # Same here
        current.note = chr(ord(current.note) + 1)        # Note name advances as well, both by name (C -> D)
        current.noteindex = (current.noteindex + 1) % 7  # as well as by number (0 -> 1)
        if current.note == "H":              # If we passed G, we must do back to A
            current.note = "A"
        elif current.note == "C":            # If we reached C, we have advanced into the next octave
            current.oct += 1
    return notes

def diatonic_distance(note, ref_note):
    """Returns the number of positions (lines/spaces) a certain note is removed from the middle staff line."""
    return note.noteindex - ref_note.noteindex + 7 * (note.oct - ref_note.oct)

def glyph(note, clef="treble", head="q", stem="", key="c"):
    key_alt = signatures[key][0]  # -1 for b keysigs, 1 for # keysigs, 0 for C/Am
    key_acc = signatures[key][1:] # list of notes that have an accidental in that key
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
            acc = "" if (key_alt == -1 and note.note in key_acc) else "b"
        case 1: 
            acc = "" if (key_alt == 1 and note.note in key_acc) else "#"
        case 0:
            acc = "n" if (key_alt and note.note in key_acc) else "" 
        case -2: 
            acc = "bb"
        case 2:
            acc = "x"
        case _:
            raise ValueError(f"Invalid accidental value: {note.alt}")
    return f"{acc}{head}{distance}{stem}"

def build_keysig(clef, key):
    if alt := signatures[key][0]:
        acc = "b" if alt == -1 else "#"
        num_acc = str(len(signatures[key][1:]))
    else:
        acc = ""
        num_acc = ""
    return clefs[clef] + acc + num_acc

def build_glyphs(notes, clef="treble", head="q", stem=True, sep=":", start="", end=":|", key="c", reversed=False):
    glyphs = []
    for note in notes:
        if g:= glyph(note, clef, head, "" if stem else "s", key):
            glyphs.append(g)
    if reversed: glyphs.reverse()
    return build_keysig(clef, key) + start + sep.join(glyphs) + end


if __name__ == "__main__":
    print("Welcome to Ambitus!")
    print("-------------------")
    choices = list(scales.keys())
    print("The following scales are available:")
    for i, scale in enumerate(choices):
        print(f"{i+1:>2}: {scale}")
    while True:
        scale = input("\nChoose a scale or press <Enter> to quit: ")
        try:
            scale = choices[int(scale)-1]
        except ValueError:
            print("Exiting...")
            exit()
        except IndexError:
            print("Choose one of these numbers:")
            for i, scale in enumerate(choices):
                print(f"{i+1:>2}: {scale}")
            continue
        while True:
            base = input("Begin scale at (default: C4)? ")
            if not base:
                base = "C4"
            end = input("End scale at or below (default: one octave above the beginning)? ")
            try:
                notes = diatonic(scale, base, end)
            except (ValueError, IndexError) as err:
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
            key = input("Which key signature, if any (e. g. F, Gm, Bb, F#m or <Enter> for C)? ").lower()
            if not key:
                key = "c"
            if key not in signatures:
                print("Invalid key signature! Choose one of the following:")
                print(", ".join(keysig.title() for keysig in signatures))
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
            remove_stem = input("Remove stems (default: No)? ")
            if remove_stem:
                if remove_stem[0].lower() == "y":
                    stem = False 
        start = input("Any additional spacing in front of the scale (one of ;:/?_ or leave blank)? ")
        end = input("Any additional characters at the end (default ':|')? ")
        if not end:
            end = ":|"
        reversed = False
        reverse_scale = input("Reverse direction (default: No)? ")
        if reverse_scale:
            if reverse_scale[0].lower() == "y":
                reversed = True 

        print()
        print(build_glyphs(notes, clef, head, stem, sep, start, end, key, reversed))
        print()



