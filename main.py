import note
from tabmaker import TabMaker
import tab


# for n in note.notes:
#     n.display_note()

tabmaker = TabMaker()

smoke = tab.Tab('smokeonthewater')
smoke.display_tab()

optimalsmoke = smoke.compress()

optimalsmoke.display_tab()

tabmaker.set_filename()

tabmaker.write_tab()
