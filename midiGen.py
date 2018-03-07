from midiutil.MidiFile import MIDIFile
import random
import numpy as np
import sys

LENGTH = 100

        #usage: mf.addNote(track, channel, pitch, time, duration, volume)
        #       mf.addTempo(track, time, 120)
        #       mf.addTrackName(track, time, "Sample Track")
        #       mf.addProgramChange(track, channel, time, program)

noteFromKey = {
    'z':36, 'x':40, 'c':44, 'v':48, 'b':52, 'n':56, 'm':60, ',':64, '.':68, '/':72,
    'a':39, 's':43, 'd':47, 'f':51, 'g':55, 'h':59, 'j':63, 'k':67, 'l':71, ';':75,
    'q':42, 'w':46, 'e':50, 'r':54, 't':58, 'y':62, 'u':66, 'i':70, 'o':74, 'p':78,
    '1':45, '2':49, '3':53, '4':57, '5':61, '6':65, '7':69, '8':73, '9':77, '0':81,
    '-':-1
}


if len(sys.argv) < 3:
    print('\nexample use:');
    print('python3 midiGen.py 120 a0220derde4rsxedxswex r0480lp-- r0480hu--\n');
    print('it means:');
    print('120             play with tempo 120');
    print('a0220derde4rsxedxswex     play argeggio (a) on half notes (02) on church organs (20) using notes derde4rsxedxswex');
    print('r0480lp--         play random (r) quarter notes (04) on ocarina (80) using lp-- notes');
    print('r0480hu--         play random (r) quarter notes (04) on ocarina (80) using hu-- notes\n');
    print('keys are notes from "Harmonic table note layout" so notes close to eachother sound good');
    print('for example lp--   is b, fis, pause, pause');
    print('and         derde4 is b, cis, fis, b, cis, a\n');
    quit()
    

mf = MIDIFile(len(sys.argv)-2)          #create tracks
mf.addTempo(0, 0, int(sys.argv[1]))
    


class Player:
    def __init__(self, trackNumber, duration, instrument, mode):
        self.trackNumber = trackNumber
        self.duration = duration
        self.instrument = instrument
        self.mode = mode
        mf.addProgramChange(trackNumber, trackNumber, 0, instrument)
        
    def generate(self, notes):
        if mode == 'a':
            for i in range(int(LENGTH / duration)):
                pitch = noteFromKey[ notes[i % len(notes)] ]
                if pitch != -1:
                    mf.addNote(trackNumber, trackNumber, pitch, i * duration, duration, 100)
        elif mode == 'r':
            for i in range(int(LENGTH / duration)):
                pitch = noteFromKey[ notes[random.randint(0, len(notes)-1)] ]
                if pitch!= -1:
                    mf.addNote(trackNumber, trackNumber, pitch, i * duration, duration, 100)


trackNumber = 0
for track in sys.argv[2:]:
    duration = 1 / int(track[1:3])
    instrument = int(track[3:5]) - 1
    notes = track[5:]
    mode = track[0]
    p = Player(trackNumber, duration, instrument, mode);
    p.generate(notes)
    
    trackNumber += 1

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)
    
