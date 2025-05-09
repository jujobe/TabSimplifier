
semitones = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B']

size = len(semitones)

notes = []

class Note:
    
    def __init__(self, ind, semitone, octave):
        
        self.ind = ind
        self.semitone = semitone
        self.octave = octave

        self.notename = self.semitone + str(self.octave)
        
    def __eq__(self, other):
        
        if isinstance(other, Note):
            return self.ind == other.ind
        return False


    def get_relative_note(self, distance):
        pos = notes.index(self)

        return notes[pos+distance]
   
    def get_relative_distance(self, note):
        pos1 = notes.index(self)
        pos2 = notes.index(note)

        return pos1 - pos2

    def to_dict(self):
        return {'ind': self.ind,
                'semitone': self.semitone,
                'octave': self.octave,
                'notename': self.notename}

    def display_note(self):
        print(f"Id = {self.ind}, Note = {self.notename}, Octave = {self.octave}, Semitone = {self.semitone}")


for i in range(0, 9):
    for j, st in enumerate(semitones):
        notes.append(Note(i*size+j, st, i))


def get_note(note):
    for n in notes:
        if n.notename == note:
            return n

    return notes[0]
