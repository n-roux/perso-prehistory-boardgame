'''
Created on 26 avr. 2018

@author: nroux
'''
GAME_VERSION = "0.0"
from gui import game_gui
if __name__ == '__main__':
        root = tk.Tk()
        game_gui(root).pack(side="top", fill="both", expand="true")
        root.title("PHBG Beta-testing tool version "+str(GAME_VERSION))
        root.mainloop()
