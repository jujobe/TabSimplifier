import note
import json
import tab

class TabMaker:
    def __init__(self):
        pass

    def set_filename(self):
        filename = input('Enter a name for the tab: ')

        self.filename = filename + ".json"


    def write_tab(self):
        tabs = {'tuning':[], 'plucks':[]}

        for i in range(7):
            if (i == 0):
                tunename = input("Enter the first tuning note(Deepest string):\nEnter 'Default' for the standard tuning: \n")
            else:
                tunename = input("Enter the next tuning note: \n")
            
            if tunename == 'Default':
                tabs['tuning'] = [x.to_dict() for x in tab.dtuning]
                break
            
            tabs['tuning'].append(note.get_note(tunename).to_dict())

        count = 0
        while True:
            if (count == 0): 
                pluck = input("Enter a pluck(string fret), seperated by space\nEnter 'S' to finish the tab.\n")
            else:
                pluck = input("next\n")

            if (pluck == 'S'):
                break

            vals = pluck.split()

            tabs.get('plucks').append(tab.Pluck(6-int(vals[0]), int(vals[1])).to_dict())

            count += 1
            

        with open(self.filename, 'w') as file:
            json.dump(tabs, file)
