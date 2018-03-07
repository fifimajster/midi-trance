from midiutil.MidiFile import MIDIFile
import random
import numpy as np
import sys

LENGTH = 1000

        
chordDictionary = {
    'a':[45,48,52], 'A':[45,49,52],
    'b':[47,50,54], 'B':[47,51,54],
    'c':[48,51,55], 'C':[48,52,55],
    'd':[50,53,57], 'D':[50,54,57],
    'e':[52,55,59], 'E':[52,56,59],
    'f':[53,57,61], 'F':[53,58,61],
    'g':[55,59,63], 'G':[55,60,63]
}


if len(sys.argv) < 4:
    print('\nexample use:');
    print('python3 midiMykMyk.py 240 80 a08C a08G r16F \n');
    print('it means:');
    print('240             play with tempo 120');
    print('80            use ocarina (80 instrument)');
    print('a08C     play argeggio (a) eight notes (04) on C chord');
    print('a08G     play arpeggio (a) eight notes (04) on G chord');
    print('r16F     play random (r) sixten notes (16) on F chord\n');
    quit()

    


class Player:
    def __init__(self, trackNumber, instrument):
        self.trackNumber = trackNumber
        self.instrument = instrument
        self.time = 0
        mf.addProgramChange(trackNumber, trackNumber, 0, instrument)
        
    def generate(self, notes, length, mode):
        if mode == 'a':
            for i in range(length):
                pitch = notes[i % len(notes)]
                if pitch != -1:
                    mf.addNote(0, 0, pitch, i + self.time, 1, 100)
        elif mode == 'r':
            for i in range(length):
                pitch = notes[random.randint(0, len(notes)-1)]
                if pitch!= -1:
                    mf.addNote(0, 0, pitch, i + self.time, 1, 100)
        self.time += length


mf = MIDIFile(1)          #create tracks
mf.addTempo(0, 0, int(sys.argv[1]))
instrument = int(sys.argv[2]) - 1
p = Player(0, instrument);

while p.time < LENGTH:
    for chordInfo in sys.argv[3:]:
        mode = chordInfo[0]
        length = int(chordInfo[1:3])
        notes = chordDictionary[chordInfo[3]]
        p.generate(notes, length, mode)
    

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)
    
