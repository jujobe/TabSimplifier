import note
import json
import math
import itertools


class Pluck:
    #I would've called it a string if it weren't for the technical difficulties it would've caused
    def __init__(self, nylon, fret): 
        self.nylon = nylon
        self.fret = fret
    
    def euclidian_distance(self, other):
        if self.fret*other.fret == 0: #If you don't need to fret there's no distance for the left hand anyway
            return 0
        return math.sqrt((self.nylon-other.nylon)**2+(self.fret-other.fret)**2)#*(max(min(self.fret*other.fret, 1), 0))

    def manhattan_distance(self, other):
        if self.fret*other.fret == 0: #If you don't need to fret there's no distance for the left hand anyway
            return 0
        return abs(self.nylon-other.nylon)+abs(self.fret-other.fret)#*(max(min(self.fret*other.fret, 1), 0))

    def to_dict(self):
        return {'nylon': self.nylon,
                'fret': self.fret}

    def __str__(self):
        return "("+str(self.nylon)+";"+str(self.fret)+")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Pluck):
            return (self.nylon == other.nylon) and (self.fret == other.fret)
        return False

    def __hash__(self):
        return hash((self.nylon, self.fret))


dtuning = [note.get_note('E2'), note.get_note('A2'), note.get_note('D3'),
           note.get_note('G3'), note.get_note('B3'), note.get_note('E4')]


class Tab:
    def __init__(self, filename, tuning = dtuning, plucks = []):
        if filename == '':
            self.tuning = list(reversed(tuning))
            self.plucks = plucks
        else:

            with open(filename + '.json', 'r') as tabfile:
                data = json.load(tabfile)
                self.tuning = []
                self.plucks = []

                for p in data.get('plucks'):
                    self.plucks.append(Pluck(p['nylon'], p['fret']))

                for t in data.get('tuning'):
                    self.tuning.append(note.get_note(t['notename']))

                self.tuning = list(reversed(self.tuning))

        self.notematrix = []
        for i, t in enumerate(self.tuning):
            self.notematrix.append([])

            for j in range(21):
                self.notematrix[i].append(t.get_relative_note(j))

    def compress(self):
        #maximum distance of semitones between tuning notes,
        #(used to determine how big chunks should be)
        maxdistance = 0
        for i in range(len(self.tuning)-1):
            curr = self.tuning[i].get_relative_distance(self.tuning[i+1])
            if curr > maxdistance:
                maxdistance = curr
        
        #Notes to hunt for
        hunted = []
        #mean center
        center = 0
        #resulting plucks
        resplucks = {}
        for p in self.plucks:
            curr = self.notematrix[p.nylon][p.fret]
            if curr not in hunted:
                hunted.append(curr)
                center += p.fret
                resplucks.update({curr.ind: p})

        # center = int(center / len(hunted))

        # print([x.notename for x in hunted])
        

        hunted_variants = {}
        #I just chuck all the ways to play the necessary notes into the dictionary
        for h in hunted:
            hunted_variants.update({h.ind:[]})
            for n, nyl in enumerate(self.notematrix):
                for s, snd in enumerate(nyl):
                    if snd == h:
                        hunted_variants[h.ind].append(Pluck(n, s))


        #Finding the least distanced combo
        possible_plucks = list(hunted_variants.values())
        all_combinations = [[]]

        #Permutation of permutations TIMES N
        for i, note_k in enumerate(possible_plucks):
            original_combinations = all_combinations.copy()
            all_combinations = []  # Clear the original list
            
            for combo in original_combinations:
                for b in range(len(note_k)):
                    # Create a deep copy of the combo
                    new_combo = [item for item in combo]  # or combo.copy()
                    # Add the corresponding note from note_k
                    new_combo.append(note_k[b])
                    # Add this new combination to all_combinations
                    all_combinations.append(new_combo)


        #Finding the combination with the least combined distance
        min_distance = 99999999
        curr_distance = 0
        curr_selection = 0
        for c, combo in enumerate(all_combinations):
            for a in combo:
                for b in combo:
                    #I should filter out duplicates but distance will be 0 anyway
                    curr_distance += a.euclidian_distance(b)

            if curr_distance < min_distance:
                min_distance = curr_distance
                curr_selection = c

            curr_distance = 0

        best_plucks = all_combinations[curr_selection]

        resoptimal = {}

        for bp in best_plucks:
            bp_note = self.notematrix[bp.nylon][bp.fret]
            
            resoptimal.update({bp_note.ind:bp})

        #Translating self.plucks with resplucks and resoptimal
        pluck_map = {}
        for key in resplucks:
            pluck_map[resplucks[key]] = resoptimal[key]

        # Now update self.plucks by replacing each item with its corresponding item from resoptimal
        new_plucks = []
        for pluck in self.plucks:
            if pluck in pluck_map:
                new_plucks.append(pluck_map[pluck])
            else:
                new_plucks.append(pluck)

        return Tab('', list(reversed(self.tuning)), new_plucks)




    def display_tab(self):
        tabmatrix = [] #Rows are strings, columns are time

        for _ in self.tuning:
            tabmatrix.append([])

        for i, p in enumerate(self.plucks):
            for j, nyl in enumerate(tabmatrix):
                app = f'-{p.fret}-' if j == p.nylon else '---'
                nyl.append(app)


        #Printing the resulting matrix:
        print('')
        for i, t in enumerate(self.tuning):
            print(f'{t.notename} |', end='')
            for j in range(len(tabmatrix[0])):
                print(tabmatrix[i][j], end='')
            print('')
        print('')
        

