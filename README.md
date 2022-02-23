# ambitus
A Python helper module for generating scales to be used with the Ambitus font

The Ambitus font provides a flexible means of generating simple musical diagrams, for example pitch ranges for vocalists, initial tunings for timpani or scales of any kind.

![image](https://user-images.githubusercontent.com/15966631/155330891-46df6175-9dbc-4ddf-8d58-e77f7058b3cf.png)

![image](https://user-images.githubusercontent.com/15966631/155327908-dade889f-4483-4a28-99ef-da90b3efaef1.png)

While the font is quite straightforward to use, building complex scales can be time-consuming. This module takes the legwork out of building different kinds of scales.

## Importing the module
Not really much to it...

    >>> import ambitus
    >>>

## Generating notes
You can generate `Note` objects by specifying its base (one of `CDEFGAB`), an optional accidental (`b` or `#`) and the octave (`1-6`). These are reflected in the `Note`s attributes `note`, `alt` (for alteration, negative values are flat, positive values are sharp), and `oct`.

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
    >>> M > N  # A#4 is higher than Cb4
    True
    >>> ambitus.Note("B3") < N  # enharmonically equivalent notes are not considered identical
    True

However, in general you don't need to generate notes individually, we want to build scales, after all!

## Generating scales
### Modal scales
The `modal()` function returns a list of `Note` objects that can later be fed into the glyph generator. 

The parameter `mode` can be set to `IONIAN` (major key), `DORIAN`, `PHRYGIAN`, `LYDIAN`, `MIXOLYDIAN`, `AEOLIAN` (melodic minor key) and `LOCRIAN`. Default is `IONIAN`.

`startkey` (defaulting to `"C3"`) can be set to any key between `Cb1` (C flat, first octave) and `"B#6"` (B sharp, 6th octave). For reference, `"C3"` is middle C.

The optional parameter `stopkey` can be set to the highest note that should not be exceeded in the scale. It defaults to the note exactly one octave above `startkey`. If you do set it, it must be higher than `startkey`.

    >>> ambitus.modal(mode=ambitus.AEOLIAN, startkey="Bb4")
    [Bb4, C5, Db5, Eb5, F5, Gb5, Ab5, Bb5]
    >>> ambitus.modal(mode=ambitus.MIXOLYDIAN, startkey="F#3", stopkey="C6")
    [F#3, G#3, A#3, B3, C#4, D#4, E4, F#4, G#4, A#4, B4, C#5, D#5, E5, F#5, G#5, A#5, B5]
    
Parameter names are optional:

    >>> ambitus.modal(ambitus.PHRYGIAN, "D2")
    [D2, Eb2, F2, G2, A2, Bb2, C3, D3]
    >>> ambitus.modal(ambitus.LOCRIAN, "Cb3")
    [Cb3, Dbb3, Ebb3, Fb3, Gbb3, Abb3, Bbb3, Cb4]

Note that it is possible to generate scales that may require glyphs like double-flat and double-sharp which are currently not supported in Ambitus.

### Additional scales
Support for chromatic scales, halftone-wholetone scales, harmonic and other minor scales is planned but not currently implemented.

## Converting scales
After you have generated a scale (or any other list of `Note` objects), you can pass that list to the `build_glyphs()` function. It will return a string that can be copied and pasted into a word processor, music notation program or any other program that can display the Ambitus font.

    >>> scale = ambitus.modal(ambitus.PHRYGIAN, "D2")
    >>> print(ambitus.build_glyphs(scale, clef="bass"))
    Bq-7:bq-6:q-5:q-4:q-3:bq-2:q-1:q:|
    
Result:
![image](https://user-images.githubusercontent.com/15966631/155335143-08796aba-f41d-4948-ba00-97e63feeb483.png)

The `build_glyphs()` function takes several parameters:

    build_glyphs(notes, clef="treble", head="q", stem=True, sep=":", start="", end=":|")
    
 - `notes` is the list of `Note` objects (required).
 - `clef` can be any of `"treble"`(default), `"bass"`, `"alto"`, or `"tenor"`. Note that Ambitus only supports glyphs up to three ledger lines off the standard staff, so if you try to write `C2` in the treble clef, no glyph will be generated, and you'll see a warning message to that effect.
 - `head` can be set to `"q"` for quarter notes (default), `"h"` for half notes, and `"w"` for whole notes.
 - `stem` is `True` by default. If you set it to `False`, quarter or half notes will be printed without a stem.
 - `sep` is the separator you want to use between notes. It defaults to `":"` which is adequate for quarter and half note scales but may be a bit narrow for whole noted scales. Other separators include (in ascending width) `"/"`, `"?"` and `"_"`. A narrower separator `";"` is also available, but probably too narrow unless your scales doesn't contain any accidentals.
 - `start` can be any string you want to include between the clef and the start of your scale, for example, an additional separator.
 - `end` is attached to the end of the string. It should contain at least one separator, and you may want to include a barline `"|"` for a single line, "||" for a double barline, and "|||" for an ending barline.
 
### Examples 

>>> scale = ambitus.modal(ambitus.MIXOLYDIAN, startkey="F#3", stopkey="C6")
>>> ambitus.build_glyphs(scale, head="w", sep="/", start=":", end="/|||")
'T:#w-0/#w-9/#w-8/w-7/#w-6/#w-5/w-4/#w-3/#w-2/#w-1/w/#w1/#w2/w3/#w4/#w5/#w6/w7/|||'
![image](https://user-images.githubusercontent.com/15966631/155342667-fe71d0ab-7711-4917-a9fc-5159d3aae9c5.png)
