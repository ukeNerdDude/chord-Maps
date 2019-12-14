#!/usr/bin/env python3
cM_Ver = "v0.1-beta"  # Initial release

""" ChordMaps.py chord map utility for stringed musical instruments.
    Copyright (C) 2019 David Murray

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


Makes a .csv fretboard for the followin stringed, fretted musical
instruments.
    Type 1: Ukulele: soprano, concert & baritone. GCEA strings.
            Entries will be checked for +/- 2 semitone limits.
    Type 2: Ukulele: baritone & four string banjo (non-tenor). DGBE strings.
            Entries will be checked for +/- 2 semitone limits.
            CGBD, DGCE and DGCD are common tuning alternatives.
    Type 3: Tenor banjo, Four strings tuned in 5ths. CGDA strings.
            Entries will be checked for +/- 2 semitone limits.
    Type 4: Banjo, five string where 5th string is a drone string independent.
            gDGBD strings. This does NOT include the drone string in the map.
            Entries will be checked for +/- 2 semitone limits.)
    Type 5: Mandolin, Four strings tuned in 5ths. GDAE strings.
            Entries will be checked for +/- 2 semitone limits.)
    Type 6: Guitar, six strings. EADGBE strings.
            Entries will be checked for +/- 2 semitone limits.)

The produced fretboard map shows the notes for Root, 3rd, 5th and 7th note
as aplicable. It is up to the user to select usable shapes for playing from
the positions shown.

First time users shold answer the first question about help comments 'Y'
"""

helpOn = False
looping = True

instType = 1
capo = 0  # fret number goes her if capo
maxFret = 27  # must not be changed to greater than 22, will throw error
chordTonic = 'C'
chordType = 5  # 0x0 = power chord, 0x1 = maj, 0x2 = min, 0x4 = 7th
chordNotes = ['', '', '', '']
chordNotesEn = ['', '', '', '']  # For fretboard map search
save2csv = True
chordName = 'C'

########################
# Setup global variables
########################

fretNumb = ('0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', '10', '11', '12', '13', '14', '15',
            '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28')
dia = (('I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V',
        'vi', 'VI', 'vii', 'VII'),
       ('C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',
       'Ab', 'A',  'Bb', 'B'),   # 0
       ('G',  'Ab', 'A', 'Bb', 'B',  'C',  'Db', 'D',
       'Eb', 'E',  'F',  'F#'),  # 1
       ('D',  'Eb', 'E', 'F',  'F#', 'G',  'Ab', 'A',
       'Bb', 'B',  'C',  'C#'),  # 2
       ('A',  'Bb', 'B', 'C',  'C#', 'D',  'Eb', 'E',
       'F',  'F#', 'G',  'G#'),  # 3
       ('E',  'F',  'F#', 'G',  'G#', 'A',  'Bb', 'B',
       'C',  'C#', 'D',  'D#'),  # 4
       ('B',  'C',  'C#', 'D',  'D#', 'E',  'F',  'F#',
       'G',  'G#', 'A',  'A#'),  # 5
       ('F#', 'G',  'G#', 'A',  'A#', 'B',  'C',  'C#',
       'D',  'D#', 'E',  'E#'),  # 6
       ('Gb', 'G',  'Ab', 'A',  'Bb', 'B',  'C',  'Db',
       'D',  'Eb', 'E',  'Fb'),  # 6 # enharmonic
       ('Db', 'D',  'Eb', 'E',  'F',  'Gb', 'G',  'Ab',
       'A',  'Bb', 'B',  'C'),   # 5 b
       ('C#', 'D',  'D#', 'E',  'F',  'F#', 'G',  'G#'
       'A',  'A#', 'B',  'C'),   # 5 b enharmonic
       ('Ab', 'A',  'Bb', 'B',  'C',  'Db', 'D',  'Eb',
       'E',  'F',  'Gb', 'G'),   # 4 b
       ('G#', 'A',  'A#', 'B',  'C',  'C#', 'D',  'D#',
       'E',  'F',  'F#', 'G'),   # 4 b enharmonic
       ('Eb', 'E',  'F',  'F#', 'G',  'Ab', 'A',  'Bb',
       'B',  'C',  'C#', 'D'),   # 3 b
       ('D#', 'E',  'F',  'F#', 'G',  'G#', 'A',  'A#',
       'B',  'C',  'C#', 'D'),   # 3 b enharmonic
       ('Bb', 'B',  'C',  'Db', 'D',  'Eb', 'E',  'F',
       'Gb', 'G',  'Ab', 'A'),   # 2 b
       ('A#', 'B',  'C',  'C#', 'D',  'D#', 'E',  'F',
       'F#', 'G',  'G#', 'A'),   # 2 b enharmonic
       ('F',  'Gb', 'G',  'Ab', 'A',  'Bb', 'B',  'C',
       'Db', 'D',  'Eb', 'E'))   # 1 b

enh = (('Db', 'Eb', 'Gb', 'Ab', 'Bb'),
       ('C#', 'D#', 'F#', 'G#', 'A#'))

# Default Type 5 EADGBE guitar
legal6 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E
legal5 = ('G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B')   # A
legal4 = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E')   # D
legal3 = ('F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
legal2 = ('A', 'A#', 'Bb', 'B', 'C',  'C#', 'Db')  # B
legal1 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E

isLegal6 = isLegal5 = isLegal4 = isLegal3 = 0
isLegal2 = isLegal1 = isLegalAll = 0

string6 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
string5 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
string4 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
string3 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
string2 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
string1 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

cstring6 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
cstring5 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
cstring4 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
cstring3 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
cstring2 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
cstring1 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']


def CreateUke():
    """
    Fills fredboad array with notes for the selected instrument and tuning
    """
    global legal6
    global legal5
    global legal4
    global legal3
    global legal2
    global legal1
    global tuning
    global maxFret
    isLegal6 = isLegal5 = isLegal4 = isLegal3 = 0
    isLegal2 = isLegal1 = isLegalAll = 0
    # Create the ukulele
    x6 = x5 = x4 = x3 = x2 = x1 = 0
    # # Will it break strings of be too floppy?
    if instType == 1:
        # tuning = ['A', 'E',  'C',  'G', '', '']  # GCEA
        legal4 = ('F',  'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
        legal3 = ('A#', 'Bb', 'B',  'C', 'C#', 'db', 'D')   # C
        legal2 = ('D',  'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E
        legal1 = ('G',  'G#', 'Ab', 'A', 'A#', 'Bb', 'B')   # A

    if instType == 2:
        # tuning = ['E', 'B', 'G', 'D', '', ''] # DGBE
        legal4 = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E')   # D
        legal3 = ('F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
        legal2 = ('A', 'A#', 'Bb', 'B', 'C',  'C#', 'Db')  # B
        legal1 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E

    if instType == 3:
        # tuning = ['A', 'D', 'G', 'C', '', ''] # CGDA
        legal4 = ('Bb', 'B',  'Cb', 'C', 'C#', 'Db', 'D')  # C
        legal3 = ('F',  'F#', 'Gb', 'G', 'G#', 'Ab', 'A')  # G
        legal2 = ('C',  'C#', 'Db', 'D', 'D#', 'Eb', 'E')  # D
        legal1 = ('G',  'G#', 'Ab', 'A', 'A#', 'Bb', 'B')  # A

    if instType == 4:
        # 5th string is G drone, independent capo or nail
        # tuning = ['E', 'B', 'G', 'D', '', ''] # DGBE
        legal4 = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E')   # D
        legal3 = ('F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
        legal2 = ('A', 'A#', 'Bb', 'B', 'C',  'C#', 'Db')  # B
        legal1 = ('D', 'D#', 'Eb', 'D', 'F',  'F#', 'Gb')  # D

    if instType == 5:
        # tuning = ['E', 'A', 'D', 'G', '', ''] # GDAE
        legal4 = ('F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
        legal3 = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E')   # D
        legal2 = ('G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B')   # A
        legal1 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E

    if instType == 6:
        # tuning = ['E', 'B', 'G',  'D', 'A', 'E'] # EADGBE
        legal6 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E
        legal5 = ('G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B')   # A
        legal4 = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E')   # D
        legal3 = ('F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A')   # G
        legal2 = ('A', 'A#', 'Bb', 'B', 'C',  'C#', 'Db')  # B
        legal1 = ('D', 'D#', 'Eb', 'E', 'F',  'F#', 'Gb')  # E

    if instType != 0:
        i = 0
        while i < 7:
            if instType == 6:
                if tuning[5] == legal6[i]:
                    isLegal6 = 1
                if tuning[4] == legal5[i]:
                    isLegal5 = 1
            if tuning[3] == legal4[i]:
                isLegal4 = 1
            if tuning[2] == legal3[i]:
                isLegal3 = 1
            if tuning[1] == legal2[i]:
                isLegal2 = 1
            if tuning[0] == legal1[i]:
                isLegal1 = 1
            i = i + 1
        isLegalAll = isLegal1 + isLegal2 + isLegal3 + isLegal4
        if isLegalAll < 4:
            print(tuning[0], tuning[1], tuning[2], tuning[3])
        if instType == 6:
            if isLegal6 == 0:
                print("WARNING: String 6 (", tuning[5], ") is more", end=' ')
                print("than +/- 2 from expected:", legal4[3])
            if isLegal5 == 0:
                print("WARNING: String 5 (", tuning[4], ") is more", end=' ')
                print("than +/- 2 from expected:", legal4[3])
        if isLegal4 == 0:
            print("WARNING: String 4 (", tuning[3], ") is more", end=' ')
            print("than +/- 2 from expected:", legal4[3])
        if isLegal3 == 0:
            print("WARNING: String 3 (", tuning[2], ")  is more", end=' ')
            print("than +/- 2 from expected:", legal3[3])
        if isLegal2 == 0:
            print("WARNING: String 2 (", tuning[1], ")  is more", end=' ')
            print("than +/- 2 from expected:", legal2[3])
        if isLegal1 == 0:
            print("WARNING: String 1 (", tuning[0], ")  is more", end=' ')
            print("than +/- 2 from expected:", legal1[3])
    i = 0  # find the offsets
    while i < len(dia):
        if tuning[0] == dia[i][0]:
            x1 = i
        if tuning[1] == dia[i][0]:
            x2 = i
        if tuning[2] == dia[i][0]:
            x3 = i
        if tuning[3] == dia[i][0]:
            x4 = i
        if instType == 6:
            if tuning[4] == dia[i][0]:
                x5 = i
            if tuning[5] == dia[i][0]:
                x6 = i
        i = i + 1
    # Create the ukulele
    i = capo
    maxCreate = maxFret + 1
    while i < maxCreate:
        string1[i] = dia[x1][i % 12]
        string2[i] = dia[x2][i % 12]
        string3[i] = dia[x3][i % 12]
        string4[i] = dia[x4][i % 12]
        if instType == 6:
            string5[i] = dia[x5][i % 12]
            string6[i] = dia[x6][i % 12]
        i = i + 1


def findChordNotes():
    """
    Finds notes for selected chord only.
    """
    global chordNotesEn
    chordNotesEn = ['', '', '', '']
    x = i = 0
    while i < len(dia):
        if dia[i][0] == chordTonic:
            x = i
        i = i + 1
    chordNotes[0] = dia[x][0]       # tonic
    if chordType & 0x1 == 1:         # major?
        chordNotes[1] = dia[x][4]
    if chordType & 0x2 == 2:         # minor?
        chordNotes[1] = dia[x][3]
    chordNotes[2] = dia[x][7]       # perfect 5th
    if chordType & 0x4 == 4:         # 7?
        chordNotes[3] = dia[x][10]
    else:
        chordNotes[3] = ''
    #
    # Enharmonic alternates
    #
    i = 0
    while i < len(enh):
        if chordNotes[0] == enh[0][i]:
            chordNotesEn[0] = enh[1][i]
        if chordNotes[0] == enh[1][i]:
            chordNotesEn[0] = enh[0][i]
        if chordNotes[1] == enh[0][i]:
            chordNotesEn[1] = enh[1][i]
        if chordNotes[1] == enh[1][i]:
            chordNotesEn[1] = enh[0][i]
        if chordNotes[2] == enh[0][i]:
            chordNotesEn[2] = enh[1][i]
        if chordNotes[2] == enh[1][i]:
            chordNotesEn[2] = enh[0][i]
        if chordNotes[3] == enh[0][i]:
            chordNotesEn[3] = enh[1][i]
        if chordNotes[3] == enh[1][i]:
            chordNotesEn[3] = enh[0][i]
        i = i + 1


def fillChordFretboard():
    """
    Fills fretboard array with notes for selected chord only.
    """
    global maxFret
    global cstring6
    global cstring5
    global cstring4
    global cstring3
    global cstring2
    global cstring1
    i = j = k = z = 0
    #
    # clear Chord Fretboard map
    #
    while z < maxFret:
        if instType == 6:
            cstring6[z] = ' '
            cstring5[z] = ' '
        cstring4[z] = ' '
        cstring3[z] = ' '
        cstring2[z] = ' '
        cstring1[z] = ' '
        z = z + 1
    #
    # Build map
    #
    i = capo
    while i < maxFret:
        while j < len(chordNotes):
            if instType == 6:
                if string6[i] == chordNotes[j]:
                    cstring6[i] = chordNotes[j]
                if string6[i] == chordNotesEn[j]:
                    cstring6[i] = chordNotes[j]
                if string5[i] == chordNotes[j]:
                    cstring5[i] = chordNotes[j]
                if string5[i] == chordNotesEn[j]:
                    cstring5[i] = chordNotes[j]
            if string4[i] == chordNotes[j]:
                cstring4[i] = chordNotes[j]
            if string4[i] == chordNotesEn[j]:
                cstring4[i] = chordNotes[j]
            if string3[i] == chordNotes[j]:
                cstring3[i] = chordNotes[j]
            if string3[i] == chordNotesEn[j]:
                cstring3[i] = chordNotes[j]
            if string2[i] == chordNotes[j]:
                cstring2[i] = chordNotes[j]
            if string2[i] == chordNotesEn[j]:
                cstring2[i] = chordNotes[j]
            if string1[i] == chordNotes[j]:
                cstring1[i] = chordNotes[j]
            if string1[i] == chordNotesEn[j]:
                cstring1[i] = chordNotes[j]
            j = j + 1
        j = 0
        i = i + 1


def printFretboard():
    """
    Writes the chord fretboard to a comman delimited file
    or displays it in console.
    """
    global maxFret
    global chordName
    global chordType
    if save2csv is True:
        fn = open(filename, "w")
    maxCreate = maxFret + 1

    # calculate chord name
    chordName = chordNotes[0]
    if chordType & 0x3 == 0:
        chordName = chordName + '5'
    if chordType & 0x1 == 1:
        chordName = chordName
    if chordType & 0x2 == 2:
        chordName = chordName + 'm'
    if chordType & 0x4 == 4:
        chordName = chordName + '7'

    # fret number
    if save2csv is True:
        fn.write(chordName)
    else:
        print(chordName, end=' ')
    i = capo
    while i < maxCreate:
        if save2csv is True:
            fn.write(",")
            fn.write(fretNumb[i])
        else:
            print(fretNumb[i], end=' ')
        i = i + 1
    if save2csv is True:
        fn.write("\n")
    else:
        print("")

    # cstring1
    if save2csv is True:
        fn.write("|")
        fn.write(tuning[0])
        fn.write("|")
    else:
        print("|", tuning[0], "|", end=' ')
    i = capo
    while i < maxCreate:
        if save2csv is True:
            fn.write(",")
            fn.write(cstring1[i])
        else:
            print(cstring1[i], end=' ')
        i = i + 1
    if save2csv is True:
        fn.write("\n")
    else:
        print("")

    # cstring2
    if save2csv is True:
        fn.write("|")
        fn.write(tuning[1])
        fn.write("|")
    else:
        print("|", tuning[1], "|", end=' ')
    i = capo
    while i < maxCreate:
        if save2csv is True:
            fn.write(",")
            fn.write(cstring2[i])
        else:
            print(cstring2[i], end=' ')
        i = i + 1
    if save2csv is True:
        fn.write("\n")
    else:
        print("")

    # cstring3
    if save2csv is True:
        fn.write("|")
        fn.write(tuning[2])
        fn.write("|")
    else:
        print("|", tuning[2], "|", end=' ')
    i = capo
    while i < maxCreate:
        if save2csv is True:
            fn.write(",")
            fn.write(cstring3[i])
        else:
            print(cstring3[i], end=' ')
        i = i + 1
    if save2csv is True:
        fn.write("\n")
    else:
        print("")

    # cstring4
    if save2csv is True:
        fn.write("|")
        fn.write(tuning[3])
        fn.write("|")
    else:
        print("|", tuning[3], "|", end=' ')
    i = capo
    while i < maxCreate:
        if save2csv is True:
            fn.write(",")
            fn.write(cstring4[i])
        else:
            print(cstring4[i], end=' ')
        i = i + 1
    if save2csv is True:
        fn.write("\n")
        if instType != 6:
            print("Results written to", filename)
    else:
        print("")
        if instType != 6:
            print("")
            print("Results NOT written to file")

    if instType == 6:

        # cstring5
        if save2csv is True:
            fn.write("|")
            fn.write(tuning[4])
            fn.write("|")
        else:
            print("|", tuning[4], "|", end=' ')
        i = capo
        while i < maxCreate:
            if save2csv is True:
                fn.write(",")
                fn.write(cstring5[i])
            else:
                print(cstring5[i], end=' ')
            i = i + 1
        if save2csv is True:
            fn.write("\n")
        else:
            print("")

        # cstring6
        if save2csv is True:
            fn.write("|")
            fn.write(tuning[5])
            fn.write("|")
        else:
            print("|", tuning[5], "|", end=' ')
        i = capo
        while i < maxCreate:
            if save2csv is True:
                fn.write(",")
                fn.write(cstring6[i])
            else:
                print(cstring6[i], end=' ')
            i = i + 1
        if save2csv is True:
            fn.write("\n")
            print("Results written to", filename)
            fn.close()
        else:
            print("")
            print("Results NOT written to file")


# main


print("")
print("    chordMaps.py  Copyright (C) 2019  David Murray")
print("    This program comes with ABSOLUTELY NO WARRANTY;")
print("    for details see GPLv3 or later.")
print("    This is free software, and you are welcome to redistribute it")
print("    under certain conditions; see GPLv3 or later for details.")
print("    GNU GPL licence at https://www.gnu.org/licenses/gpl-3.0.en.html")
print("")

#
# help?
#
x = input("Turn on help comments (N,y)?") or 'N'
if x == 'Y' or x == 'y':
    helpOn = True

#
# instType
#
if helpOn is True:
    print("")
    print("chordMaps.py", cM_Ver)
    print("")
    print("Type 1: Ukulele: soprano, concert & baritone. No", end=' ')
    print("distinction for high-G vs. low-G strings.")
    print("        GCEA is the assumed string set and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Type 2: Ukulele: baritone. Four string banjo", end=' ')
    print("(non-tenor): no drone string.")
    print("        DGBE is the assumed string set and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Type 3: Tenor banjo, Four strings tuned in 5ths.")
    print("        CGDA is the assumed string set and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Type 4: Banjo, five string where 5th string", end=' ')
    print("is a drone string and is not shown in the result.")
    print("        gDGBD is the assumed string set  and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Type 5: Mandolin, Four strings tuned in 5ths.")
    print("        GDAE is the assumed string set and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Type 6: Guitar, six strings. This is the only", end=' ')
    print("type that maps more than 4 strings.")
    print("        EADGBE is the assumed string set and", end=' ')
    print("entries will be checked for +/- 2 semitone limits.")
    print("Note: selectio that excedes the +/-2 limit generates", end=' ')
    print("a warning but does not prevent map creation.")
    print("      Hopefully you have chosen an appropriate", end=' ')
    print("string guage for any choice with a warning.")
    print("")

x = '9'
while int(x) < 1 or int(x) > 6:
    print("Instrument type (1=ukulele, 2=baritone", end=' ')
    print("3=tenor banjo, 4=banjo, 5=mandolin, 6=guitar)?", end=' ')
    x = input() or '9'
instType = int(x)
# set defaults
if instType == 1:
    tuning = ['A', 'E', 'C', 'G', '', '']    # GCEA ukulele
if instType == 2:
    tuning = ['E', 'B', 'G', 'D', '', '']    # DGBE baratone ukulele
if instType == 3:
    tuning = ['A', 'D', 'G', 'C', '', '']    # CGDA tenor banjo
if instType == 4:
    tuning = ['D', 'B', 'G', 'D', '', '']    # DGBD banjo
if instType == 5:
    tuning = ['E', 'A', 'D', 'G', '', '']    # GDAE mandolin
if instType == 6:
    tuning = ['E', 'B', 'G', 'D', 'A', 'E']  # EADGBE guitar

#
# capo
#
if helpOn is True:
    print("")
    print("If you are using a capo, enter the fret", end=' ')
    print("number it will be placed at.")
    print("If you are not using a capo, enter 0 or", end=' ')
    print("press 'Enter' with no entry.")
    print("")

capo = 12
while capo > 11:
    x = input("Capo (0=none(default) or fret number)?") or '0'
    capo = int(x)
maxFret = 15 + capo

#
# change tuning?
#
if helpOn is True:
    print("")
    print("You may alter the tuning here or accept the default for no change.")
    print("Choices start at", end=' ')
    if instType == 6:
        print(tuning[5], tuning[4], end=' ')
    print(tuning[3], tuning[2], tuning[1], "->", tuning[0], end=' ')
    print("<- where string number is ukulele order (highest note = 1)")
    print("")

CreateUke()  # 1st call

print("Change string 1", tuning[0], "to (enter=no change", end=' ')
print("or enter case sensitive note)?", end=' ')
x = input() or tuning[0]
tuning[0] = x
print("Change string 2", tuning[1], "to (enter=no change", end=' ')
print("or enter case sensitive note)?", end=' ')
x = input() or tuning[1]
tuning[1] = x
print("Change string 3", tuning[2], "to (enter=no change", end=' ')
print("or enter case sensitive note)?", end=' ')
x = input() or tuning[2]
tuning[2] = x
print("Change string 4", tuning[3], "to (enter=no change", end=' ')
print("or enter case sensitive note)?", end=' ')
x = input() or tuning[3]
tuning[3] = x
if instType == 6:
    print("Change string 5", tuning[4], "to (enter=no change", end=' ')
    print("or enter case sensitive note)?", end=' ')
    x = input() or tuning[4]
    tuning[4] = x
    print("Change string 6", tuning[5], "to (enter=no change", end=' ')
    print("or enter case sensitive note)?", end=' ')
    x = input() or tuning[5]
    tuning[5] = x

#
# Start chord entry loop
#
while looping is True:
    if helpOn is True:
        print("")
        print("Enter the note as Ab, A, A#, Bb, B, C, C#, Db, etc.", end=' ')
        print("(case sensitive)")
        print("The choices which follow will be for major, minor, etc.")
        print("")

    chordTonic = 'z'
    while chordTonic == 'z':
        x = input("Chord tonic/root note (case sensitive)?") or 'z'
        chordTonic = x
#
# chord type
#
    if helpOn is True:
        print("")
        print("Major=1-M3-5, minor=1-b3-5, power chord=1-5 (no 3rd,", end=' ')
        print("neither major or minor)")
        print("")

    chordType = 9
    while chordType == 9:
        x = input("Chord type (1=major, 2=minor, 0=power chord)?") or '9'
        chordType = int(x)

    if chordType != 0:
        if helpOn is True:
            print("")
            print("7 chord=1-3-5-b7")
            print("")

        x = 'z'
        while x == '7' or (x != 'Y' and x != 'y' and x != 'N' and x != 'n'):
            x = input("Add 7th to chord (N or y)?") or 'N'
        if str.upper(x) == 'Y':
            chordType = chordType | 4

    CreateUke()
    findChordNotes()
    fillChordFretboard()
#    print ("Chord", chordNotes)

#
# save to csv?
#
    if instType == 6:
        filename = tuning[5] + tuning[4] + tuning[3] + tuning[2]
        filename = filename + tuning[1] + tuning[0]
    else:
        filename = tuning[3] + tuning[2] + tuning[1] + tuning[0]
    filename = filename + "_" + str(capo) + "_" + chordNotes[0]
    if chordNotes[1] == '':
        filename = filename + '-'
    else:
        filename = filename + chordNotes[1]
    filename = filename + chordNotes[2]
    if chordNotes[3] == '':
        filename = filename + '-'
    else:
        filename = filename + chordNotes[3]
    filename = filename + '.csv'

    if helpOn is True:
        print("")
        print("Fret board maps to a .csv file which can be imported")
        print("to a standard spreadsheet program for formatting.")
        print("The default writes the .csv file, selecting 'n'")
        print("displays the unformatted output that would have been written.")
        print("The file name indicates what was mapped tuning_capo_chord.csv")
        print("")

    print("Save to", filename, "(Y or n)?", end=' ')
    x = input() or 'Y'
    if str.upper(x) == 'Y':
        save2csv = True
    else:
        save2csv = False

    printFretboard()

    if helpOn is True:
        print("")
        print("You may do different chords with the same tuning or quit.")
        print("")

    x = input("Another chord? (Y,n)?") or 'Y'
    if x == 'N' or x == 'n':
        looping = False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
