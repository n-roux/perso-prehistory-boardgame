'''
Created on 26 avr. 2018

@author: nroux
'''
import Tkinter as tk

GAME_VERSION = "0.0"
from gui import SoloBetatestGUI

if __name__ == '__main__':
        root = tk.Tk()
        SoloBetatestGUI(root).pack(side="top", fill="both", expand="true")
        root.title("PHBG Beta-testing tool version "+str(GAME_VERSION))
        root.mainloop()
