# ambitus.py
**A Python helper module for generating scales to be used with the Ambitus font**

The Ambitus font provides a flexible means of generating simple musical diagrams, for example pitch ranges for vocalists, initial tunings for timpani or scales of any kind.

![image](https://user-images.githubusercontent.com/15966631/155330891-46df6175-9dbc-4ddf-8d58-e77f7058b3cf.png)

![image](https://user-images.githubusercontent.com/15966631/155327908-dade889f-4483-4a28-99ef-da90b3efaef1.png)

While the font is quite straightforward to use, building complex scales can be time-consuming. This module takes the legwork out of building different kinds of scales.

## Importing the module
Not really much to it...
```python
>>> import ambitus
```
## Generating notes
You can generate `Note` objects by specifying its base (one of `CDEFGAB`), an optional accidental (`b` or `#`) and the octave (`1-6`). These are reflected in the `Note`s attributes `note`, `alt` (for alteration, negative values are flat, positive values are sharp), and `oct`.

```python
>>> N = ambitus.Note("Cb4")
>>> N.note
'C'
>>> N.alt
-1
>>> N.oct
4
>>> print(N)
Cb4
>>> M = ambitus.Note("A#4")
>>> M > N                   # A#4 is higher than Cb4
True
>>> ambitus.Note("B3") < N  # enharmonically equivalent notes are not considered identical
True
```

However, in general you don't need to generate notes individually, we want to build scales, after all!

## Generating scales
### Diatonic scales
The `diatonic()` function returns a list of `Note` objects that can later be fed into the glyph generator. 

```python
diatonic(scale="Major", startkey="C4", stopkey="")
```

The parameter `scale` can be set to [one of the following values](https://en.wikipedia.org/wiki/Jazz_scale): 
 - `"Major"`
 - `"Natural minor"`
 - `"Harmonic minor"`
 - `"Aeolian"`
 - `"Locrian"`
 - `"Ionian"`
 - `"Lydian"`
 - `"Dorian"`
 - `"Phrygian"`
 - `"Mixolydian"`
 - `"Melodic minor"`
 - `"Phrygian n6"`
 - `"Lydian augmented"`
 - `"Lydian dominant"`
 - `"Mixolydian b6"`
 - `"Locrian n2"`
 - `"Altered dominant"`

`startkey` defaults to `"C4"` but can be set to any note between `Cb1` (C flat, first octave) and `"B#6"` (B sharp, 6th octave). For reference, `"C4"` is middle C.

The optional parameter `stopkey` can be set to a different note in the same range and determines where the scale will end. It defaults to the note exactly one octave above `startkey`. If you set `stopkey` below `startkey`, the scale will be constructed downwards (useful for minor scales, for example – harmonic minor for the ascending scale, melodic minor for the descending scale). If you choose a `stopkey` that isn't part of the scale (like `C#5` when building a C major scale from `C4`), scale construction will end before passing that note (`C5` in this example).

```python
>>> ambitus.diatonic(scale="Aeolian", startkey="Bb4")
[Bb4, C5, Db5, Eb5, F5, Gb5, Ab5, Bb5]
>>> ambitus.diatonic(scale="Mixolydian", startkey="F#3", stopkey="C6")
[F#3, G#3, A#3, B3, C#4, D#4, E4, F#4, G#4, A#4, B4, C#5, D#5, E5, F#5, G#5, A#5, B5]
```

Parameter names are optional:

```python
>>> ambitus.diatonic("Phrygian", "D2")
[D2, Eb2, F2, G2, A2, Bb2, C3, D3]
```

### Additional scales
Support for chromatic, halftone-wholetone, pentatonic, blues scales and possibly others is planned but not currently implemented.

## Converting scales
After you have generated a scale (or any other list of `Note` objects), you can pass that list to the `build_glyphs()` function. It will return a string that can be copied and pasted into a word processor, music notation program or any other program that can display the Ambitus font.

```python
>>> scale = ambitus.diatonic("Phrygian", "D2")
>>> print(ambitus.build_glyphs(scale, clef="bass"))
Bq-7:bq-6:q-5:q-4:q-3:bq-2:q-1:q:|
```

Result:
![image](https://user-images.githubusercontent.com/15966631/155335143-08796aba-f41d-4948-ba00-97e63feeb483.png)

The `build_glyphs()` function takes several parameters:

```python
build_glyphs(notes, clef="treble", head="q", stem=True, sep=":", start="", end=":|")
```

 - `notes` is the list of `Note` objects (required).
 - `clef` can be any of `"treble"`(default), `"bass"`, `"alto"`, or `"tenor"`. Note that Ambitus only supports glyphs up to three ledger lines off the standard staff, so if you try to write `C2` in the treble clef, no glyph will be generated, and you'll see a warning message to that effect.
 - `head` can be set to `"q"` for quarter notes (default), `"h"` for half notes, and `"w"` for whole notes.
 - `stem` is `True` by default. If you set it to `False`, quarter or half notes will be printed without a stem.
 - `sep` is the separator you want to use between notes. It defaults to `":"` which is adequate for quarter and half note scales but may be a bit narrow for whole noted scales. Other separators include (in ascending width) `"/"`, `"?"` and `"_"`. A narrower separator `";"` is also available, but probably too narrow unless your scales doesn't contain any accidentals.
 - `start` can be any string you want to include between the clef and the start of your scale, for example, an additional separator.
 - `end` is attached to the end of the string. It should contain at least one separator, and you may want to include a barline `"|"` for a single line, `"||"` for a double barline, and `"|||"` for an ending barline.
 
### Examples 
```python
>>> scale = ambitus.diatonic()          # Simple example with default parameters: C major
>>> print(ambitus.build_glyphs(scale))  # Default "rendering" parameters: quarter notes with stems
Tq-6:q-5:q-4:q-3:q-2:q-1:q:q1:|
```

![image](https://user-images.githubusercontent.com/15966631/155388245-1ebfc6ee-3b2f-48e5-a02a-a70f0eb057ac.png)

```python
>>> scale = ambitus.diatonic("Locrian", "Cb4")
>>> print(scale)
[Cb4, Dbb4, Ebb4, Fb4, Gbb4, Abb4, Bbb4, Cb5]
>>> print(ambitus.build_glyphs(scale, sep="/", start=":"))
T:bq-6/bbq-5/bbq-4/bq-3/bbq-2/bbq-1/bbq/bq1:|
```
![image](https://user-images.githubusercontent.com/15966631/155738916-46bf4f5a-0ca3-4191-92f8-7ccb81224c33.png)

```python
>>> scale = ambitus.diatonic("Mixolydian", startkey="F#3", stopkey="C6")
>>> ambitus.build_glyphs(scale, head="w", sep="/", start=":", end="/|||")
'T:#w-0/#w-9/#w-8/w-7/#w-6/#w-5/w-4/#w-3/#w-2/#w-1/w/#w1/#w2/w3/#w4/#w5/#w6/w7/|||'
```

![image](https://user-images.githubusercontent.com/15966631/155342667-fe71d0ab-7711-4917-a9fc-5159d3aae9c5.png)

```python
>>> scale = ambitus.diatonic("Lydian", "D4")
>>> print(ambitus.build_glyphs(scale, clef="alto", head="q", stem=False))
Aq1s:q2s:#q3s:#q4s:q5s:q6s:#q7s:q8s:|
```

![image](https://user-images.githubusercontent.com/15966631/155372250-c8cfae73-9ad1-4121-b4b9-6b697597e6e1.png)


### Interactive mode

If you run the module from the command line instead of importing it, you can build scales interactively.

Here's an example session:

    > python ambitus.py
    Welcome to Ambitus!
    -------------------
    The following scales are available:
     1: Major
     2: Natural minor
     3: Harmonic minor
     4: Aeolian
     5: Locrian
     6: Ionian
     7: Lydian
     8: Dorian
     9: Phrygian
    10: Mixolydian
    11: Melodic minor
    12: Phrygian n6
    13: Lydian augmented
    14: Lydian dominant
    15: Mixolydian b6
    16: Locrian n2
    17: Altered dominant

    Choose a scale or press <Enter> to quit: 1
    Begin scale at (default: C4)? A4
    End scale at or below (default: one octave above the beginning)? A6
    Scale:  [A4, B4, C#5, D5, E5, F#5, G#5, A5, B5, C#6, D6, E6, F#6, G#6, A6]
    Which clef should be used (treble (default), bass, alto or tenor)? trble
    Invalid clef!
    Which clef should be used (treble (default), bass, alto or tenor)? treble
    Choose separator (one of ;:/?_ (default ':')) /
    Choose notehead (one of q (default), h, w) h
    Remove stems (default: No)? y
    Any additional spacing in front of the scale (;:/?_ or leave blank)? 
    Any additional characters at the end (default ':|')
    Note F#6 out of range for treble clef (Fb3-E#6)
    Note G#6 out of range for treble clef (Fb3-E#6)
    Note A6 out of range for treble clef (Fb3-E#6)
    Th-1s/hs/#h1s/h2s/h3s/#h4s/#h5s/h6s/h7s/#h8s/h9s/h0s:|
    
    Choose a scale or press <Enter> to quit: 1
    Exiting...

Result:
![image](https://user-images.githubusercontent.com/15966631/155371282-6963c2e9-3d79-4597-a17a-3065db8fdb7c.png)

