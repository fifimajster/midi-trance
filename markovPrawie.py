from midiutil.MidiFile import MIDIFile
import random
import sys

import hashlib
import mido

from markov_chain import MarkovChain

LENGTH = 100



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


class Parser:

    def __init__(self, filename):
        self.filename = filename
        self.markov_chain = MarkovChain()
        
        midi = mido.MidiFile(self.filename)
        previous_note = 0
        for track in midi.tracks:
            for message in track:
               if message.type == "note_on":
                   current_note = (message.note)%12
                   self.markov_chain.add(previous_note, current_note, 0)
                   previous_note = current_note


    def get_chain(self):
        return self.markov_chain

Parser(sys.argv[1])
print(Parser.get_chain())

# write it to disk
with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)
    
