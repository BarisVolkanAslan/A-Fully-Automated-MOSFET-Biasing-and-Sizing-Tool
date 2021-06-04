# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:40:12 2021
VSB
@author: Baris
"""

import sys
import os.path
libdir = os.path.dirname(__file__)
sys.path.append(os.path.split(libdir)[0])   
from Libraries import start_gui

try:
    start_gui.create_dirs()
    start_gui.start_screen()
    start_gui.root.mainloop()
except:
    start_gui.error()

