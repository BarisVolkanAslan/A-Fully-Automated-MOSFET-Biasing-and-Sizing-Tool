# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 19:30:33 2021

@author: Baris
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk,Image
import os
import sys
import ctypes

libdir = os.path.dirname(__file__)
sys.path.append(os.path.split(libdir)[0])   
from Libraries import bsim_gui
from Libraries import umc_gui
from Libraries import bsim_ng_base
from Libraries import tsmc_gui

global icon_path 
global flowchart_path 
global yeditepe_path

icon_path = 'Program Images/logo.ico'
flowchart_path = "Program Images/flowchart.png"
yeditepe_path = "Program Images/yeditepe.png"

def create_dirs():
    FILE_ATTRIBUTE_HIDDEN = 0x02
    CURR_DIR = os.getcwd()
    
    database_FOLDER = CURR_DIR + "/Database"
    images_FOLDER = CURR_DIR + "/Images"
    bsim_simulations_FOLDER = images_FOLDER + "/BSIM Simulations"
    tsmc_simulations_FOLDER = images_FOLDER + "/TSMC Simulations"
    umc_simulations_FOLDER = images_FOLDER + "/UMC Simulations"
    sim_data_FOLDER = CURR_DIR + "/sim_data"
    bsim_FOLDER = sim_data_FOLDER + "/BSIM"
    tsmc_FOLDER = sim_data_FOLDER + "/TSMC"
    umc_FOLDER = sim_data_FOLDER + "/UMC"
    
    if not os.path.isdir(database_FOLDER):
       os.makedirs(database_FOLDER)
       ctypes.windll.kernel32.SetFileAttributesW(database_FOLDER, FILE_ATTRIBUTE_HIDDEN)
    if not os.path.isdir(images_FOLDER):
       os.makedirs(images_FOLDER)
       ctypes.windll.kernel32.SetFileAttributesW(images_FOLDER, FILE_ATTRIBUTE_HIDDEN)
       os.makedirs(bsim_simulations_FOLDER)
       os.makedirs(tsmc_simulations_FOLDER)
       os.makedirs(umc_simulations_FOLDER)

    if not os.path.isdir(sim_data_FOLDER):
       os.makedirs(sim_data_FOLDER)
       ctypes.windll.kernel32.SetFileAttributesW(sim_data_FOLDER, FILE_ATTRIBUTE_HIDDEN)
       os.makedirs(bsim_FOLDER)
       os.makedirs(umc_FOLDER)
       os.makedirs(tsmc_FOLDER)
       
# Place a root in to the center of a screen.
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()   


# Create a root for start screen interface
def start_screen():
    global root
    root = tk.Tk()
    root.title("Microelectronics Laboratory : MOSFET Biasing and Sizing Tool")
    root.iconbitmap(icon_path)
    root.geometry("532x660")
    root.configure(background='white')
    center(root)
    
    # YEDITEPE UNIVERSITY LOGO
    global yeditepe
    yeditepe = ImageTk.PhotoImage(Image.open(yeditepe_path))
    tk.Label(image = yeditepe, background='white').grid(row=0, column=0)     
    
    # BOOK LABEL
    tk.Label(root, background='white', font=('Times',10) ,text="Cilingiroglu, Ugur (2019) ‘Analog Integrated Circuit Design by Simulation: \n Techniques, Tools, and Methods’, McGraw-Hill Education").grid(row=1,column=0)
    
    #FIGURE 3.24
    global flowchart
    flowchart = ImageTk.PhotoImage(Image.open(flowchart_path))
    tk.Label(image = flowchart, background='white').grid(row=2, column=0) 
    tk.Label(root, text="Figure 3.24 Flowchart of relations in a saturated MOSFET.", background='white', font=('Times',10)).grid(row=3,column=0)


    # SELECT MODEL DECK
    global clicked_model_deck
    global model_decks
    global model_deck_combo
    model_decks = [
    "BSIM3v3.2 Model Deck",
    "TSMC Model Deck",
    "UMC Model Deck"
    ]
    
    tk.Label(root, text="Please select a model deck.", background='white').grid(row=4,column=0)
    model_deck_combo = ttk.Combobox(root,value=model_decks)
    model_deck_combo.current(0)
    model_deck_combo.grid(row=5, column=0, columnspan=2, pady=6, padx=10, ipadx=10)

    
    # INITIALIZE SIMULATION BUTTON
    tk.Button(root, text="Initialize Simulation", command=chose_model_deck).grid(row=6, column=0, columnspan=2, pady=50, padx=10, ipadx=32, ipady=10)  
        
def chose_model_deck():
    if(model_deck_combo.get() == model_decks[0]):
        bsim_ng_base.bsim_sp(1)
        bsim_gui.initialize()         
    elif(model_deck_combo.get() == model_decks[1]):
        tsmc_gui.initialize() 
    elif(model_deck_combo.get() == model_decks[2]):
        umc_gui.initialize() 
        
def error():
    messagebox.showerror("Fatal Error", "404 Not Found")  


