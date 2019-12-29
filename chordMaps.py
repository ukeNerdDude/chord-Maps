#!/usr/bin/env python3
#  Ver = "v0.1-beta"  # Initial release
#  Ver = "v0.2-beta"  # User input poofing,
#                     # add feature, print to csv shows capo tuning
#  Ver = "v0.3-beta"  # enharmonic bug fix,
#  Ver = "v0.4-beta"  # missing comma in C# tupple bug fix,
#  Ver = "v0.5-beta"  # added banjo drone,
#                     # abandoned PEP8 80 char line limit for readability
#  Ver = v0.6-beta"  # removed || from file write,
#                     # removed v0.2 frint to csv capo tuning
#  Ver = "v0.7-beta"  # added choice of pentatonic mode
#  Ver = "v0.8-beta"  # added choice of scales
cM_Ver = "v0.9-beta"  # removed debug print statements (hase makes waste)
#  ToDo 1. compact modes with simiar funtions. For now durring beta, leaving
#          seperate for debugging/fault isolaion purpose
#       2. complete user input error trapping

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
            gDGBD strings. v0.5 adds drone sting (does not affect chord shapes).
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
chordType = 5  # 0x0 = power, 0x1 = maj, 0x2 = min, 0x4 = 7th, 0x8 = pent
chordNotes = ['', '', '', '']
chordNotesEn = ['', '', '', '']  # For fretboard map search
scaleType = 0
pent = 2  # C&W Major
pentNotes = ['', '', '', '', '']
pentNotesEn = ['', '', '', '', '']
mode = 1  # Ionian
modalNotes = ['', '', '', '', '', '', '']
modalNotesEn = ['', '', '', '', '', '', '']
mtnMnNotes = ['', '', '', '', '', '']
mtnMnNotesEn = ['', '', '', '', '', '']
save2csv = True
chordName = 'C'
fifthEntered = 'g'
droneNote = ['d', 'd#', 'e', 'f', 'f#', 'g',  'g#', 'a', 'a#', 'b',  'c',  'c#']
droneString = ['', '', '', '', '', '',  '', '', '', '',  '',  '']
droneCapo = 5  # aka fret 5 (no capo), expected spike 7, 9, 10
at5 = 'g'
tuning = ['', '', '', '']
tuningN = ['', '', '', '']

########################
# Setup global variables
########################

fretNumb = ('0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', '10', '11', '12', '13', '14', '15',
            '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28')
dia = (('I', 'ii', 'II', 'iii', 'III', 'IV', 'v', 'V', 'vi', 'VI', 'vii', 'VII'),
       ('C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G', 'Ab', 'A',  'Bb', 'B'),
       ('G',  'Ab', 'A', 'Bb', 'B',  'C',  'Db', 'D', 'Eb', 'E',  'F',  'F#'),
       ('D',  'Eb', 'E', 'F',  'F#', 'G',  'Ab', 'A', 'Bb', 'B',  'C',  'C#'),
       ('A',  'Bb', 'B', 'C',  'C#', 'D',  'Eb', 'E', 'F',  'F#', 'G',  'G#'),
       ('E',  'F',  'F#', 'G',  'G#', 'A',  'Bb', 'B', 'C',  'C#', 'D',  'D#'),
       ('B',  'C',  'C#', 'D',  'D#', 'E',  'F',  'F#', 'G',  'G#', 'A',  'A#'),
       ('F#', 'G',  'G#', 'A',  'A#', 'B',  'C',  'C#', 'D',  'D#', 'E',  'E#'),
       ('Gb', 'G',  'Ab', 'A',  'Bb', 'B',  'C',  'Db', 'D',  'Eb', 'E',  'Fb'),
       ('Db', 'D',  'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A',  'Bb', 'B',  'C'),
       ('C#', 'D',  'D#', 'E',  'F',  'F#', 'G',  'G#', 'A',  'A#', 'B',  'C'),
       ('Ab', 'A',  'Bb', 'B',  'C',  'Db', 'D',  'Eb', 'E',  'F',  'Gb', 'G'),
       ('G#', 'A',  'A#', 'B',  'C',  'C#', 'D',  'D#', 'E',  'F',  'F#', 'G'),
       ('Eb', 'E',  'F',  'F#', 'G',  'Ab', 'A',  'Bb', 'B',  'C',  'C#', 'D'),
       ('D#', 'E',  'F',  'F#', 'G',  'G#', 'A',  'A#', 'B',  'C',  'C#', 'D'),
       ('Bb', 'B',  'C',  'Db', 'D',  'Eb', 'E',  'F', 'Gb', 'G',  'Ab', 'A'),
       ('A#', 'B',  'C',  'C#', 'D',  'D#', 'E',  'F', 'F#', 'G',  'G#', 'A'),
       ('F',  'Gb', 'G',  'Ab', 'A',  'Bb', 'B',  'C', 'Db', 'D',  'Eb', 'E'))

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
    isLegalDrone = 0
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
            if instType == 4:
                if fifthEntered.upper() == legal3[i]:
                    isLegalDrone = 1
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
        if instType == 4:
            if isLegalDrone == 0:
                print("WARNING: Drone string (", fifthEntered, ") is more", end=' ')
                print("than +/- 2 from expected:", legal3[3].lower())
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
    i = 0
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
    global chordNotes
    global chordNotesEn
    chordNotesEn = ['', '', '', '']
    x = i = 0
    while i < len(dia):
        if dia[i][0] == chordTonic:
            x = i
        i = i + 1
    chordNotes[0] = dia[x][0]
    if chordType & 0x1 == 1:
        chordNotes[1] = dia[x][4]
    if chordType & 0x2 == 2:
        chordNotes[1] = dia[x][3]
    chordNotes[2] = dia[x][7]
    if chordType & 0x4 == 4:
        chordNotes[3] = dia[x][10]
    else:
        chordNotes[3] = ''
    #
    # Enharmonic alternates
    #
    i = 0
    while i < 5:  # v0.3 enharmonic bug fix
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


def findModeNotes():
    """
    Finds notes of selected diatonic modal scale  # feature added v0.8
    """
    global mode
    global modalNotes
    global modalNotesEn
    modalNotesEn = ['', '', '', '', '', '', '']
    x = i = 0
    while i < len(dia):
        if dia[i][0] == chordTonic:  # use chordTonic
            x = i
        i = i + 1
    if mode == 1:  # ionian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][2]
        modalNotes[2] = dia[x][4]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][9]
        modalNotes[6] = dia[x][11]
    if mode == 2:  # mixolydian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][2]
        modalNotes[2] = dia[x][4]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][9]
        modalNotes[6] = dia[x][10]
    if mode == 3:  # dorian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][2]
        modalNotes[2] = dia[x][3]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][9]
        modalNotes[6] = dia[x][10]
    if mode == 4:  # aeolian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][2]
        modalNotes[2] = dia[x][3]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][8]
        modalNotes[6] = dia[x][10]
    if mode == 5:  # phrygian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][1]
        modalNotes[2] = dia[x][3]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][8]
        modalNotes[6] = dia[x][10]
    if mode == 6:  # locrian
        modalNotes[0] = dia[x][0]
        modalNotes[2] = dia[x][1]
        modalNotes[1] = dia[x][3]
        modalNotes[3] = dia[x][5]
        modalNotes[4] = dia[x][6]
        modalNotes[5] = dia[x][8]
        modalNotes[6] = dia[x][10]
    if mode == 7:  # lydian
        modalNotes[0] = dia[x][0]
        modalNotes[1] = dia[x][2]
        modalNotes[2] = dia[x][4]
        modalNotes[3] = dia[x][6]
        modalNotes[4] = dia[x][7]
        modalNotes[5] = dia[x][9]
        modalNotes[6] = dia[x][11]
    #
    # Enharmonic alternates
    #
    i = 0
    while i < 5:
        if modalNotes[0] == enh[0][i]:
            modalNotesEn[0] = enh[1][i]
        if modalNotes[0] == enh[1][i]:
            modalNotesEn[0] = enh[0][i]
        if modalNotes[1] == enh[0][i]:
            modalNotesEn[1] = enh[1][i]
        if modalNotes[1] == enh[1][i]:
            modalNotesEn[1] = enh[0][i]
        if modalNotes[2] == enh[0][i]:
            modalNotesEn[2] = enh[1][i]
        if modalNotes[2] == enh[1][i]:
            modalNotesEn[2] = enh[0][i]
        if modalNotes[3] == enh[0][i]:
            modalNotesEn[3] = enh[1][i]
        if modalNotes[3] == enh[1][i]:
            modalNotesEn[3] = enh[0][i]
        if modalNotes[4] == enh[0][i]:
            modalNotesEn[4] = enh[1][i]
        if modalNotes[4] == enh[1][i]:
            modalNotesEn[4] = enh[0][i]
        if modalNotes[5] == enh[0][i]:
            modalNotesEn[5] = enh[1][i]
        if modalNotes[5] == enh[1][i]:
            modalNotesEn[5] = enh[0][i]
        if modalNotes[6] == enh[0][i]:
            modalNotesEn[6] = enh[1][i]
        if modalNotes[6] == enh[1][i]:
            modalNotesEn[6] = enh[0][i]
        i = i + 1


def findMountainMinorNotes():
    """
    Finds notes of selected mountain minor scale  # feature added v0.8
    """
    global mtnMnNotes
    global mtnMnNotesEn
    mtnMnNotesEn = ['', '', '', '', '', '']
    x = i = 0
    while i < len(dia):
        if dia[i][0] == chordTonic:  # use chordTonic
            x = i
        i = i + 1
    mtnMnNotes[0] = dia[x][0]
    mtnMnNotes[1] = dia[x][2]
    mtnMnNotes[2] = dia[x][3]
    mtnMnNotes[3] = dia[x][5]
    mtnMnNotes[4] = dia[x][7]
    mtnMnNotes[5] = dia[x][10]
    #
    # Enharmonic alternates
    #
    i = 0
    while i < 5:
        if mtnMnNotes[0] == enh[0][i]:
            mtnMnNotesEn[0] = enh[1][i]
        if mtnMnNotes[0] == enh[1][i]:
            mtnMnNotesEn[0] = enh[0][i]
        if mtnMnNotes[1] == enh[0][i]:
            mtnMnNotesEn[1] = enh[1][i]
        if mtnMnNotes[1] == enh[1][i]:
            mtnMnNotesEn[1] = enh[0][i]
        if mtnMnNotes[2] == enh[0][i]:
            mtnMnNotesEn[2] = enh[1][i]
        if mtnMnNotes[2] == enh[1][i]:
            mtnMnNotesEn[2] = enh[0][i]
        if mtnMnNotes[3] == enh[0][i]:
            mtnMnNotesEn[3] = enh[1][i]
        if mtnMnNotes[3] == enh[1][i]:
            mtnMnNotesEn[3] = enh[0][i]
        if mtnMnNotes[4] == enh[0][i]:
            mtnMnNotesEn[4] = enh[1][i]
        if mtnMnNotes[4] == enh[1][i]:
            mtnMnNotesEn[4] = enh[0][i]
        if mtnMnNotes[5] == enh[0][i]:
            mtnMnNotesEn[5] = enh[1][i]
        if mtnMnNotes[5] == enh[1][i]:
            mtnMnNotesEn[5] = enh[0][i]
        i = i + 1


def findPentNotes():  # Feature added in v0.3
    """
    Finds notes for selected pentatonic scale.
    """
    global pent
    global pentNotes
    global pentNotesEn
    pentNotesEn = ['', '', '', '', '']
    x = i = 0
    while i < len(dia):
        if dia[i][0] == chordTonic:  # use chordTonic
            x = i
        i = i + 1
    #  anhemitonic (no semitones) pentatonics formed by dropping the
    #  semitones from the 'from' mode. 'also' overlays
    if pent == 1:  # blues minor from phrygian, also dorian & aeolian
        pentNotes[0] = dia[x][0]
        pentNotes[1] = dia[x][3]
        pentNotes[2] = dia[x][5]
        pentNotes[3] = dia[x][7]
        pentNotes[4] = dia[x][10]
    if pent == 2:  # major from mixolydian, also lydian & ionian
        pentNotes[0] = dia[x][0]
        pentNotes[1] = dia[x][2]
        pentNotes[2] = dia[x][4]
        pentNotes[3] = dia[x][7]
        pentNotes[4] = dia[x][9]
    if pent == 3:  # appalachian from aeolian, also mixolydian & dorian
        pentNotes[0] = dia[x][0]
        pentNotes[1] = dia[x][2]
        pentNotes[2] = dia[x][5]
        pentNotes[3] = dia[x][7]
        pentNotes[4] = dia[x][10]
    if pent == 4:  # fifthless from locrian, also aeolian & phrygian
        pentNotes[0] = dia[x][0]
        pentNotes[1] = dia[x][3]
        pentNotes[2] = dia[x][5]
        pentNotes[3] = dia[x][8]
        pentNotes[4] = dia[x][10]
    if pent == 5:  # chinese from dorian, also ionian & mixolydian
        pentNotes[0] = dia[x][0]
        pentNotes[1] = dia[x][2]
        pentNotes[2] = dia[x][5]
        pentNotes[3] = dia[x][7]
        pentNotes[4] = dia[x][9]
    #
    # Enharmonic alternates
    #
    i = 0
    while i < 5:
        if pentNotes[0] == enh[0][i]:
            pentNotesEn[0] = enh[1][i]
        if pentNotes[0] == enh[1][i]:
            pentNotesEn[0] = enh[0][i]
        if pentNotes[1] == enh[0][i]:
            pentNotesEn[1] = enh[1][i]
        if pentNotes[1] == enh[1][i]:
            pentNotesEn[1] = enh[0][i]
        if pentNotes[2] == enh[0][i]:
            pentNotesEn[2] = enh[1][i]
        if pentNotes[2] == enh[1][i]:
            pentNotesEn[2] = enh[0][i]
        if pentNotes[3] == enh[0][i]:
            pentNotesEn[3] = enh[1][i]
        if pentNotes[3] == enh[1][i]:
            pentNotesEn[3] = enh[0][i]
        if pentNotes[4] == enh[0][i]:
            pentNotesEn[4] = enh[1][i]
        if pentNotes[4] == enh[1][i]:
            pentNotesEn[4] = enh[0][i]
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
    maxCreate = maxFret + 1  # v0.3 missing last col data bug fix
    while z < maxCreate:
        if instType == 6:
            cstring6[z] = ' '
            cstring5[z] = ' '
        if instType == 4:
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
    while i < maxCreate:
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
            if instType == 4:
                string5[i] = ''
                if i < 12:
                    string5[i] = droneString[i]
                    cstring5[i] = droneString[i]
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


def fillPentFretboard():
    """
    Fills fretboard array with notes for selected pentatonic scale.
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
    maxCreate = maxFret + 1  # v0.3 max column bug fix
    while z < maxCreate:
        if instType == 6:
            cstring6[z] = ' '
            cstring5[z] = ' '
        if instType == 4:
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
    while i < maxCreate:
        while j < len(pentNotes):
            if instType == 6:
                if string6[i] == pentNotes[j]:
                    cstring6[i] = pentNotes[j]
                if string6[i] == pentNotesEn[j]:
                    cstring6[i] = pentNotes[j]
                if string5[i] == pentNotes[j]:
                    cstring5[i] = pentNotes[j]
                if string5[i] == pentNotesEn[j]:
                    cstring5[i] = pentNotes[j]
            if instType == 4:
                string5[i] = ' '
                if i < 12:
                    string5[i] = droneString[i]
                    cstring5[i] = droneString[i]
            if string4[i] == pentNotes[j]:
                cstring4[i] = pentNotes[j]
            if string4[i] == pentNotesEn[j]:
                cstring4[i] = pentNotes[j]
            if string3[i] == pentNotes[j]:
                cstring3[i] = pentNotes[j]
            if string3[i] == pentNotesEn[j]:
                cstring3[i] = pentNotes[j]
            if string2[i] == pentNotes[j]:
                cstring2[i] = pentNotes[j]
            if string2[i] == pentNotesEn[j]:
                cstring2[i] = pentNotes[j]
            if string1[i] == pentNotes[j]:
                cstring1[i] = pentNotes[j]
            if string1[i] == pentNotesEn[j]:
                cstring1[i] = pentNotes[j]
            j = j + 1
        j = 0
        i = i + 1


def fillModalFretboard():
    """
    Fills fretboard array with notes for selected modal scale.
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
    # clear Fretboard map
    #
    maxCreate = maxFret + 1
    while z < maxCreate:
        if instType == 6:
            cstring6[z] = ' '
            cstring5[z] = ' '
        if instType == 4:
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
    while i < maxCreate:
        while j < len(modalNotes):
            if instType == 6:
                if string6[i] == modalNotes[j]:
                    cstring6[i] = modalNotes[j]
                if string6[i] == modalNotesEn[j]:
                    cstring6[i] = modalNotes[j]
                if string5[i] == modalNotes[j]:
                    cstring5[i] = modalNotes[j]
                if string5[i] == modalNotesEn[j]:
                    cstring5[i] = modalNotes[j]
            if instType == 4:
                string5[i] = ' '
                if i < 12:
                    string5[i] = droneString[i]
                    cstring5[i] = droneString[i]
            if string4[i] == modalNotes[j]:
                cstring4[i] = modalNotes[j]
            if string4[i] == modalNotesEn[j]:
                cstring4[i] = modalNotes[j]
            if string3[i] == modalNotes[j]:
                cstring3[i] = modalNotes[j]
            if string3[i] == modalNotesEn[j]:
                cstring3[i] = modalNotes[j]
            if string2[i] == modalNotes[j]:
                cstring2[i] = modalNotes[j]
            if string2[i] == modalNotesEn[j]:
                cstring2[i] = modalNotes[j]
            if string1[i] == modalNotes[j]:
                cstring1[i] = modalNotes[j]
            if string1[i] == modalNotesEn[j]:
                cstring1[i] = modalNotes[j]
            j = j + 1
        j = 0
        i = i + 1


def fillMtnMnFretboard():
    """
    Fills fretboard array with notes for selected modal scale.
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
    # clear Fretboard map
    #
    maxCreate = maxFret + 1
    while z < maxCreate:
        if instType == 6:
            cstring6[z] = ' '
            cstring5[z] = ' '
        if instType == 4:
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
    while i < maxCreate:
        while j < len(mtnMnNotes):
            if instType == 6:
                if string6[i] == mtnMnNotes[j]:
                    cstring6[i] = mtnMnNotes[j]
                if string6[i] == mtnMnNotesEn[j]:
                    cstring6[i] = mtnMnNotes[j]
                if string5[i] == mtnMnNotes[j]:
                    cstring5[i] = mtnMnNotes[j]
                if string5[i] == mtnMnNotesEn[j]:
                    cstring5[i] = mtnMnNotes[j]
            if instType == 4:
                string5[i] = ' '
                if i < 12:
                    string5[i] = droneString[i]
                    cstring5[i] = droneString[i]
            if string4[i] == mtnMnNotes[j]:
                cstring4[i] = mtnMnNotes[j]
            if string4[i] == mtnMnNotesEn[j]:
                cstring4[i] = mtnMnNotes[j]
            if string3[i] == mtnMnNotes[j]:
                cstring3[i] = mtnMnNotes[j]
            if string3[i] == mtnMnNotesEn[j]:
                cstring3[i] = mtnMnNotes[j]
            if string2[i] == mtnMnNotes[j]:
                cstring2[i] = mtnMnNotes[j]
            if string2[i] == mtnMnNotesEn[j]:
                cstring2[i] = mtnMnNotes[j]
            if string1[i] == mtnMnNotes[j]:
                cstring1[i] = mtnMnNotes[j]
            if string1[i] == mtnMnNotesEn[j]:
                cstring1[i] = mtnMnNotes[j]
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
    global scaleType
    if save2csv is True:
        fn = open(filename, "w")
    maxCreate = maxFret + 1

    # calculate chord name
    chordName = chordNotes[0]
    if chordType != 8:
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
        #  v0.2 show capo'd tuning
        #  v0.6 removed showing capo'd tuning
        fn.write(tuning[0])
    else:  # displa not updated for capo
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
        #  v0.2 show capo'd tuning
        #  v0.6 removed showing capo'd tuning
        fn.write(tuning[1])
    else:  # displa not updated for capo
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
        #  v0.2 show capo'd tuning
        #  v0.6 removed showing capo'd tuning
        fn.write(tuning[2])
    else:  # displa not updated for capo
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
        #  v0.2 show capo'd tuning
        #  v0.6 removed showing capo'd tuning
        fn.write(tuning[3])
    else:  # displa not updated for capo
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
        if instType != 6 and instType != 4:
            print("Results written to", filename)
    else:
        print("")
        if instType != 6 and instType != 4:
            print("")
            print("Results NOT written to file")

    if instType == 4:
        #  Banjo cstring5
        i = 0
        if save2csv is True:
            fn.write(droneString[droneCapo])
        else:
            print("|", droneString[droneCapo], "|", end=' ')
        while i < maxCreate:
            if save2csv is True:
                fn.write(",")
                fn.write(cstring5[i])
            else:
                print(cstring5[i], end=' ')
            i = i + 1
        if save2csv is True:
            fn.write("\n")
            if instType == 4:
                print("Results written to", filename)
        else:
            print("")
            if instType == 4:
                print("")
                print("Results NOT written to file")

    if instType == 6:

        # cstring5
        if save2csv is True:
            #  v0.2 show capo'd tuning
            #  v0.6 removed showing capo'd tuning
            fn.write(tuning[4])
        else:  # displa not updated for capo
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
            #  v0.2 show capo'd tuning
            fn.write(tuning[5])
        else:  # displa not updated for capo
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
            if capo > 0:  # v0.2
                print("Results show tuning as capo tuning.")
            fn.close()
        else:
            print("")
            print("Results NOT written to file")

######
# main
######


print("")
print("    chordMaps.py  Copyright (C) 2019  David Murray", cM_Ver)
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
    print("is a drone string, shown but does not affect chord shapes.")
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
    #  v0.2 catch alpha input
    if x.isalpha():
        x = 9
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
    droneCapo = 5    # default is no capo
if instType == 5:
    tuning = ['E', 'A', 'D', 'G', '', '']    # GDAE mandolin
if instType == 6:
    tuning = ['E', 'B', 'G', 'D', 'A', 'E']  # EADGBE guitar

#
# capos
#
if helpOn is True:
    print("")
    print("If you are using a capo, enter the fret", end=' ')
    print("number it will be placed at.")
    print("If you are not using a capo, enter 0 or", end=' ')
    print("press 'Enter' with no entry.")

capo = 12
while capo > 11:
    x = input("Capo (0=none(default) or fret number)?") or '0'
    #  v0.2 catch alpha input
    if x.isalpha():
        capo = 12
    else:
        capo = int(x)
maxFret = 15 + capo

print("")
if helpOn is True:
    if instType == 4:
        print("Changing the tuning of the drone string is")
        print("normally only done if you have no capo or spike.")
        print("")

if instType == 4:
    fifthEntered = 'g'
    droneCapo = 5
    x = 'z'
    nLoc = 0
    sa = 0
    print("Banjo drone string")
    while x == 'z':
        print("Change drone string", 'g', "to (enter=no change", end=' ')
        print("or enter note)?", end=' ')
        x = input() or 'g'
        x = x.lower()
        k = 0
        i = 0
        #  ('Db', 'Eb', 'Gb', 'Ab', 'Bb')
        #  ('C#', 'D#', 'F#', 'G#', 'A#')
        while i < 5:
            if x == 'Db' or x == 'db' or x == 'C#':
                x = 'c#'
            if x == 'Eb' or x == 'eb' or x == 'D#':
                x = 'd#'
            if x == 'Gb' or x == 'gb' or x == 'F#':
                x = 'f#'
            if x == 'Ab' or x == 'ab' or x == 'G#':
                x = 'g#'
            if x == 'Bb' or x == 'bb' or x == 'A#':
                x = 'a#'
            i = i + 1
        while k < 12:
            if x == droneNote[k]:
                nLoc = k
            k = k + 1
    fifthentered = x
    at5 = x
    #  adjust scale for entered fifthEntered
    if nLoc != 5:
        adjVal = nLoc - 5
        z = 0
        if adjVal > 0:
            #  higher pitch
            zz = adjVal
            while z < 12:
                droneString[z] = droneNote[zz % 12]
                z = z + 1
                zz = zz + 1
        else:
            #  lower pitch
            zz = (adjVal + 12) % 12
            while z < 12:
                droneString[z] = droneNote[zz % 12]
                z = z + 1
                zz = zz + 1
        z = 0
        while z < 12:
            droneNote[z] = droneString[z]
            z = z + 1

    if helpOn is True:
        if instType == 4:
            print("")
            print("Banjo 5th string drone capo or spike fret number.")
            print("5 = no capo, capoing up 2 = 7 for the 7th fret, etc.")
            print("")

    x = 12
    y = 12
    while x == 12:
        print("Enter 5th string capo fret number (default is 5=no capo:", end=' ')
        y = input() or '5'
        x = int(y)
        if int(x) < 5 or int(x) > 11:
            x = 12
    droneCapo = int(y)

    #  fill droneString
    i = 0
    while i < 12:
        if i == 5:
            droneString[i] = at5
        elif i == droneCapo:
            droneString[i] = droneNote[i]
        else:
            droneString[i] = ''
        i = i + 1
    print("Banjo drone string end")
    print("")
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
tuningN = tuning

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
    chordNotes[0] = chordTonic  # this is for pentatonic
#
# chord type
#
    if helpOn is True:
        print("")
        print("Major=1-M3-5, minor=1-b3-5, power chord=1-5 (no 3rd,", end=' ')
        print("neither major or minor), scale=select a scale scale.")
        print("")

    chordType = 9
    while chordType == 9:
        print("Chord type (0=pwr chord, 1=major, 2=minor, 8=scale)?", end=' ')
        x = input() or '9'
        chordType = int(x)
        if chordType != 0 and chordType != 1 and chordType != 2 and chordType != 8:
            chordType = 9
    if chordType != 8:
        if chordType != 0:
            if helpOn is True:
                print("")
                print("7 chord=1-3-5-b7")
                print("")
            x = 'z'
            while x == '7' or (x.upper() != 'Y' and x.upper() != 'N'):
                x = input("Add 7th to chord (N or y)?") or 'N'
            if str.upper(x) == 'Y':
                chordType = chordType | 4
    CreateUke()
    if chordType < 8:
        findChordNotes()
        fillChordFretboard()
    else:
        whatScale = 14
        zzz = ''
        if helpOn is True:
            print("")
            print("Pentatonic modes are anhemitonic modes 1-5")
            print("Diatonic modes are Ionian, Mixolydian, Dorian, etc.")
            print("Mountain Minor is the old-time I, II, bIII, IV, V, bVII scale")
            print("")
        while whatScale == 14:
            print("1=Pent 1, 2=pent 2, 3=pent 3, 4=pent 4, 5=pent 5")
            print("6=Ionian, 7=Mixolydian, 8=Dorian, 9=Aeolian")
            print("10=Phtygian, 11=Locrian, 12=Lydian, 13=Mountain Minor")
            print("Enter the scale want", end=' ')
            zzz = input()
            whatScale = int(zzz)
            if whatScale < 1 or whatScale > 13:
                whatScale = 14
            else:
                scaleType = whatScale
        if whatScale < 6:
            pent = whatScale
            findPentNotes()
            fillPentFretboard()
        elif whatScale == 13:
            findMountainMinorNotes()
            fillMtnMnFretboard()
        else:
            mode = whatScale - 5
            findModeNotes()
            fillModalFretboard()


#
# save to csv?
#
    if instType == 4:
        filename = droneString[droneCapo] + tuning[3]
        filename = filename + tuning[2] + tuning[1] + tuning[0]
    elif instType == 6:
        filename = tuning[5] + tuning[4] + tuning[3] + tuning[2]
        filename = filename + tuning[1] + tuning[0]
    else:
        filename = tuning[3] + tuning[2] + tuning[1] + tuning[0]
    filename = filename + "_" + str(capo) + "_" + chordNotes[0]
    if chordType == 8:
        if scaleType < 6:
            filename = filename + "-pent" + str(pent)
        if scaleType == 6:
            filename = filename + "-ion"
        if scaleType == 7:
            filename = filename + "-mix"
        if scaleType == 8:
            filename = filename + "-dor"
        if scaleType == 9:
            filename = filename + "-aeo"
        if scaleType == 10:
            filename = filename + "-phy"
        if scaleType == 11:
            filename = filename + "-loc"
        if scaleType == 12:
            filename = filename + "-lyd"
        if scaleType == 13:
            filename = filename + "-mtnMn"
    else:
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
