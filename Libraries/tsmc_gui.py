# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 19:30:33 2021

@author: Baris
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk,Image
import shutil
import sqlite3
import os
import sys

libdir = os.path.dirname(__file__)
sys.path.append(os.path.split(libdir)[0])   
from Libraries import tsmc_ng
from Libraries import tsmc_ng_func
from Libraries import tsmc_ng_base
from Libraries import start_gui

ng_base  = tsmc_ng_base 
ng_func = tsmc_ng_func
ng = tsmc_ng

""" FUNCTIONS """
# Define global paths of the program environment.
def define_global_paths():
    global open_icon_path
    global icon_path
    global img_path 
    global database_path
    global raw_data_path
    global n_verify_txt_path
    global p_verify_txt_path
    global sim_option_speed
    global sim_option
    
    sim_option_speed = 0
    sim_option = 0
    raw_data_path = 'sim_data/TSMC/'
    open_icon_path = 'Program Images/open.ico'
    icon_path = 'Program Images/logo.ico'
    img_path = "Images/TSMC Simulations/simulation.png"
    database_path = "Database/program_inputs_tsmc.db"
    n_verify_txt_path = 'n_results.txt'
    p_verify_txt_path = 'p_results.txt'

# Yes or No popup message.
def areyousure():
    return messagebox.askyesno("",""" This will delete selected record.
                               Are you sure?""")     

# Information about the program and how to use it appropriately. 
def info_button():
    information = """
    Information will be added soon.
    
    """
    messagebox.showinfo("Information", information)  

# Call the simulated graphical data saved as png.
def simulation_image():   
    enable_out_boxes()
    if(out_Wdr.get()):
        disable_out_boxes()
        root_img = tk.Tk()
        root_img.title("Simulation Results")
        root_img.iconbitmap(icon_path)
        root_img.geometry("900x850")      
        root_img.configure(background='white')
        start_gui.center(root_img)    
        
        global simulation
        sim_img = Image.open(img_path)
        resizedImage = sim_img.resize((855, 820), Image.ANTIALIAS)
        simulation = ImageTk.PhotoImage(resizedImage, master=root_img)
        
        tk.Label(root_img, image = simulation, background='white').grid(row=7, column=0)
    else:
        disable_out_boxes()
        messagebox.showwarning("Warning", "Please run a simulation first.")

def open_file():
    global model_deck_loc
    model_deck_loc = filedialog.askopenfilename(initialdir="/", title="Select A File", \
                                                  filetypes=(("sp files", "*.sp"),       \
                                                             ("lib files", "*.lib"),     \
                                                             ("all files", "*.*")))
    if(model_deck_loc != "") :
        inp_model_deck.configure(state= tk.NORMAL)  
        inp_model_deck.delete(0, tk.END)
        inp_model_deck.insert(0, model_deck_loc)
        inp_model_deck.configure(state= tk.DISABLED)    
    return

def open_file_edit():
    global model_deck_loc_edt
    model_deck_loc_edt = filedialog.askopenfilename(initialdir="/", title="Select A File", \
                                                  filetypes=(("sp files", "*.sp"),       \
                                                             ("lib files", "*.lib"),     \
                                                             ("all files", "*.*")))
    if(model_deck_loc_edt != "") :
        edt_model_deck.configure(state= tk.NORMAL)  
        edt_model_deck.delete(0, tk.END)
        edt_model_deck.insert(0, model_deck_loc_edt)
        edt_model_deck.configure(state= tk.DISABLED)        
    return

    
""" ROOTS """
# Create a root for simulation interface.
def initialize():   
    root = tk.Tk()
    root.title("Microelectronics Laboratory : MOSFET Biasing and Sizing Tool - TSMC Model Decks")
    root.iconbitmap(icon_path)
    root.geometry("1495x685")       
    start_gui.center(root)  
    
    #Database
    global Database_File
    Database_File = database_path
    # Create a database or connect to one
    global conn
    conn = sqlite3.connect(Database_File)
    # Create cursor
    global c
    c = conn.cursor()
    
    #Create a database table
    try:
        c.execute(""" CREATE TABLE inputs(
                database_name text,
                model_deck text,
                model text,
                Ldrmin float,
                Wdrmin float,
                Vdsat float,
                gm float,
                gmb float,
                rds float,
                Id float,
                Vsb float,
                Vds float,
                Vgs float,
                Ldr float
                )""")
    except:
        messagebox.showinfo("Information", "TSMC Database file was already created.") 
        
  
        
    """
    ###########################
    # CREATE DATA INPUT FRAME #
    ###########################
    """
    global inp_frame
    inp_frame = tk.LabelFrame(root, text="DATA INPUTS", padx=30, pady=16, bd = 5, labelanchor = 'n', font = "none 15 bold")
    inp_frame.grid(column=0, row=0, padx=10, pady=20) 
    

    # APPLICATION SPESIFICS FRAME
    tk.Label(inp_frame, text="APPLICATION SPESIFICS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=0)
    # Create Application Spesifics Text Box Labels
    tk.Label(inp_frame, text="Model deck").grid(row=1, column=0, sticky=tk.E)   #Type model
    tk.Label(inp_frame, text="Type .model").grid(row=2, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type Ldr(min)").grid(row=3, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type Wdr(min)").grid(row=4, column=0, sticky=tk.E)
    # Create Application Spesifics Text Boxes
    global inp_model_deck
    global inp_model
    global inp_Ldrmin
    global inp_Wdrmin
    inp_model_deck = tk.Entry(inp_frame, width=30)
    inp_model_deck.grid(row=1, column=1, padx=20)
    inp_model_deck.insert(0, "Locate a TSMC model deck file.")
    inp_model_deck.configure(state= tk.DISABLED)
    
    inp_model = tk.Entry(inp_frame, width=30)
    inp_model.grid(row=2, column=1, padx=20)    
    inp_Ldrmin = tk.Entry(inp_frame, width=30)
    inp_Ldrmin.grid(row=3, column=1, padx=20) 
    inp_Wdrmin = tk.Entry(inp_frame, width=30)
    inp_Wdrmin.grid(row=4, column=1, padx=20) 
    # Create Units and Examples
    global open_btn
    img = Image.open(open_icon_path)
    resizedImage = img.resize((25, 25), Image.ANTIALIAS)
    open_btn = ImageTk.PhotoImage(resizedImage, master=root)
    tk.Button(inp_frame, image=open_btn, command=open_file, borderwidth=0).grid(row=1, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(ex: cmosn)").grid(row=2, column=2, sticky=tk.W) 
    tk.Label(inp_frame, text="(\N{MICRO SIGN}m)").grid(row=3, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(\N{MICRO SIGN}m)").grid(row=4, column=2, sticky=tk.W)
    tk.Label(inp_frame, text=" ").grid(column=1, row=5)
    
    # PERFORMANCE METRICS FRAME    
    tk.Label(inp_frame, text="PERFORMANCE METRICS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=6)
    # Create Performance Metrics Text Box Labels
    tk.Label(inp_frame, text="Type Vdsat").grid(row=7, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type gm").grid(row=8, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type gmb").grid(row=9, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type rds").grid(row=10, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type Id").grid(row=11, column=0, sticky=tk.E)
    # Create Performance Metrics Text Boxes    
    global inp_Vdsat
    global inp_gm
    global inp_gmb
    global inp_rds
    global inp_Id
    inp_Vdsat = tk.Entry(inp_frame, width=30)
    inp_Vdsat.grid(row=7, column=1, padx=20)
    inp_gm = tk.Entry(inp_frame, width=30)
    inp_gm.grid(row=8, column=1, padx=20)
    inp_gmb = tk.Entry(inp_frame, width=30)
    inp_gmb.grid(row=9, column=1, padx=20)
    inp_rds = tk.Entry(inp_frame, width=30)
    inp_rds.grid(row=10, column=1, padx=20)
    inp_Id = tk.Entry(inp_frame, width=30)
    inp_Id.grid(row=11, column=1, padx=20)   
    # Create Units and Examples
    tk.Label(inp_frame, text="(V)").grid(row=7, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(mA/V)").grid(row=8, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(mA/V)").grid(row=9, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(k\u03A9)").grid(row=10, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(\N{MICRO SIGN}A)").grid(row=11, column=2, sticky=tk.W)
    tk.Label(inp_frame, text=" ").grid(column=1, row=12)
    

    # BIAS VOLTAGES FRAME
    tk.Label(inp_frame, text="EXTERNALLY IMPOSED BIAS VOLTAGES", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=13)
    # Create Bias Voltages Text Box Labels
    tk.Label(inp_frame, text="Type Vsb").grid(row=14, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type Vds").grid(row=15, column=0, sticky=tk.E)
    tk.Label(inp_frame, text="Type Vgs").grid(row=16, column=0, sticky=tk.E)
    # Create Bias Voltages Text Boxes 
    global inp_Vsb
    global inp_Vds
    global inp_Vgs
    inp_Vsb = tk.Entry(inp_frame, width=30)
    inp_Vsb.grid(row=14, column=1, padx=20)
    inp_Vds = tk.Entry(inp_frame, width=30) 
    inp_Vds.grid(row=15, column=1, padx=20)
    inp_Vgs = tk.Entry(inp_frame, width=30) 
    inp_Vgs.grid(row=16, column=1, padx=20)
    # Create Units and Examples
    tk.Label(inp_frame, text="(V)").grid(row=14, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(V)").grid(row=15, column=2, sticky=tk.W)
    tk.Label(inp_frame, text="(V)").grid(row=16, column=2, sticky=tk.W)
    tk.Label(inp_frame, text=" ").grid(column=1, row=17)
    
   # INITIAL GUESS FRAME    
    tk.Label(inp_frame, text="INITIAL GUESS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=18)
    # Create Initial Guess Text Box Labels
    tk.Label(inp_frame, text="Type initial Ldr").grid(row=19, column=0, sticky=tk.E) #initial guess
    # Create Initial Guess Text Boxes 
    global inp_Ldr
    inp_Ldr = tk.Entry(inp_frame, width=30)
    inp_Ldr.grid(row=19, column=1, padx=20)
    # Create Units and Examples
    tk.Label(inp_frame, text="(\N{MICRO SIGN}m)").grid(row=19, column=2, sticky=tk.W)
    tk.Label(inp_frame, text=" ").grid(column=1, row=20)
    
    # INPUT BUTTONS
    # Create Info Button
    tk.Button(inp_frame, text="Information", command=info_button).grid(row=21, column=0, columnspan=3, pady=6, padx=10, ipadx=146)
    # Create Clear Button
    tk.Button(inp_frame, text="Clear", command=clear_boxes).grid(row=22, column=0, columnspan=3, pady=6, padx=10, ipadx=163)
    # Create Check Errors Button
    tk.Button(inp_frame, text="Check", command=error_checker_inp).grid(row=23, column=0, columnspan=3, pady=6, padx=10, ipadx=160)
    
    """
    ###########################
    #  CREATE DATABASE FRAME  #
    ###########################
    """    
    Simulation_frame = tk.LabelFrame(root, padx=0, pady=0, bd = 0)
    Simulation_frame.grid(column=1, row=0, padx=20, pady=20)
    
    # DATABASE FRAME
    database_frame = tk.LabelFrame(Simulation_frame, 
                                     padx=38, pady=10, bd = 0,text="CONFIGURE DATABASE",
                                     labelanchor = 'n', font = "none 13 bold")
    database_frame.grid(column=0, row=0, padx=0, pady=2)
    global database_name
    database_name = tk.Entry(database_frame, width=30)
    database_name.grid(row=0, column=1, padx=20, pady=(0,0))
    # Simulation name
    tk.Label(database_frame, text="Declare a simulation name").grid(row=0, column=0, pady=(0,0), sticky=tk.E)
    # Create Submit Button
    tk.Button(database_frame, text="Add Inputs to Local Database", command=database_submit_inp).grid(row=1, column=0, columnspan=2, pady=6, padx=10, ipadx=100)
    # Create a Query Button
    tk.Button(database_frame, text="Show Local Records", command=database_query).grid(row=2, column=0, columnspan=2, pady=6, padx=10, ipadx=125)
    #  Select ID Box 
    tk.Label(database_frame, text="Select ID Number").grid(row=3, column=0)
    # Create Select ID Texts
    global database_select_box  
    database_select_box = tk.Entry(database_frame, width=30)
    database_select_box.grid(row=3, column=1)
    # Create a Select Button
    tk.Button(database_frame, text="Select Local Record", command=database_get_inp).grid(row=4, column=0, columnspan=2, pady=6, padx=10, ipadx=125)
    # Create a Delete Button
    tk.Button(database_frame, text="Delete Local Record", command=database_delete).grid(row=5, column=0, columnspan=2, pady=6, padx=10, ipadx=125)
    # Create an Edit Button
    tk.Button(database_frame, text="Edit Local Record", command=database_edit).grid(row=6, column=0, columnspan=2, pady=6, padx=10, ipadx=132)
    
    # RUN BUTTON
    tk.LabelFrame(Simulation_frame, bd = 0, pady=10).grid(row=2, column=0) 
    tk.Button(Simulation_frame, text=">>>>> RUN >>>>>", command=simulate, font = "Bold 20").grid(row=1, column=0, pady=10, padx=0, ipadx=30, ipady=30)
    tk.Button(Simulation_frame, text="OPTIONS", command=options, font = "Bold 12").grid(row=2, column=0, columnspan=2, pady=6, padx=10, ipadx=118)

    

          

    """
    ############################
    # CREATE DATA OUTPUT FRAME #
    ############################
    """
    out_frame = tk.LabelFrame(root, text="DATA OUTPUTS", padx=35, pady=105, bd = 5, labelanchor = 'n', font = "none 15 bold")
    out_frame.grid(column=2, row=0, padx=5, pady=20)
    
    # CREATE APPLICATION SPESIFICS FRAME
    tk.Label(out_frame, text="MODEL DECK VALUES", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=0) 
    # Create Text Box Labels
    tk.Label(out_frame, text="LINT").grid(row=1, column=0, sticky=tk.E)
    tk.Label(out_frame, text="WINT").grid(row=2, column=0, sticky=tk.E)
    tk.Label(out_frame, text="XL").grid(row=3, column=0, sticky=tk.E)
    tk.Label(out_frame, text="XW").grid(row=4, column=0, sticky=tk.E)
    # Create Text Boxes
    global out_LINT
    global out_WINT
    global out_XL
    global out_XW
    out_LINT = tk.Entry(out_frame, width=30)
    out_LINT.grid(row=1, column=1, padx=20)
    out_WINT = tk.Entry(out_frame, width=30)
    out_WINT.grid(row=2, column=1, padx=20)
    out_XL = tk.Entry(out_frame, width=30)
    out_XL.grid(row=3, column=1, padx=20)
    out_XW = tk.Entry(out_frame, width=30)
    out_XW.grid(row=4, column=1, padx=20)
    #emptry line
    tk.Label(out_frame, text=" ").grid(column=1, row=5)  


    # CREATE DESIGN VARIABLES FRAME
    tk.Label(out_frame, text="DESIGN VARIABLES", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=6)  
    # Create Text Box Labels
    tk.Label(out_frame, text="Ldr").grid(row=7, column=0, sticky=tk.E)
    tk.Label(out_frame, text="Wdr").grid(row=8, column=0, sticky=tk.E)
    # Create Text Boxes
    global out_Ldr
    global out_Wdr
    out_Ldr = tk.Entry(out_frame, width=30)
    out_Ldr.grid(row=7, column=1, padx=20)
    out_Wdr = tk.Entry(out_frame, width=30)
    out_Wdr.grid(row=8, column=1, padx=20)
    #Create Units    
    tk.Label(out_frame, text="(\N{MICRO SIGN}m)").grid(row=7, column=2, sticky=tk.W)
    tk.Label(out_frame, text="(\N{MICRO SIGN}m)").grid(row=8, column=2, sticky=tk.W)
    tk.Label(out_frame, text=" ").grid(column=1, row=9)  
        
    
    # CREATE BIAS VOLTAGES FRAME
    tk.Label(out_frame, text="BIAS VOLTAGES", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=10)  
    # Create Text Box Labels
    tk.Label(out_frame, text="Vsb").grid(row=11, column=0, sticky=tk.E)
    tk.Label(out_frame, text="Vds").grid(row=12, column=0, sticky=tk.E)
    tk.Label(out_frame, text="Vgs").grid(row=13, column=0, sticky=tk.E)
    # Create Text Boxes
    global out_Vsb
    global out_Vds
    global out_Vgs
    out_Vsb = tk.Entry(out_frame, width=30)
    out_Vsb.grid(row=11, column=1, padx=20)
    out_Vds = tk.Entry(out_frame, width=30)
    out_Vds.grid(row=12, column=1, padx=20)
    out_Vgs = tk.Entry(out_frame, width=30)
    out_Vgs.grid(row=13, column=1, padx=20)
    #Create Units    
    tk.Label(out_frame, text="(V)").grid(row=11, column=2, sticky=tk.W)
    tk.Label(out_frame, text="(V)").grid(row=12, column=2, sticky=tk.W)
    tk.Label(out_frame, text="(V)").grid(row=13, column=2, sticky=tk.W)
    tk.Label(out_frame, text=" ").grid(column=1, row=14)
    
    tk.Button(out_frame, text="Iterations", command=simulation_image).grid(row=15, column=0, columnspan=3, pady=6, padx=10, ipadx=145)
    tk.Button(out_frame, text="Verification", command=verification).grid(row=16, column=0, columnspan=3, pady=6, padx=10, ipadx=140)
    
    disable_out_boxes()
    global vds_toggle
    vds_toggle = 0
    global vsb_toggle
    vsb_toggle = 0
    global sim_option
    sim_option = 0 #use vds and vsb while extracting raw_data from figures

    """
    CLOSE DATABASE
    """
    # Comit Changes
    conn.commit()
    # Close Connection
    conn.close()
    root.mainloop()

# Create a root for simulation results.
def initialize_verification():
    global ver_root
    ver_root = tk.Tk()
    ver_root.title("Verification Results")
    ver_root.iconbitmap(icon_path)
    ver_root.geometry("445x234")   
    start_gui.center(ver_root)
    
    global ver_frame
    ver_frame = tk.LabelFrame(ver_root, padx=50, pady=20, bd = 0, labelanchor = 'n', font = "none 15 bold")
    ver_frame.grid(column=0, row=0, padx=10, pady=20) 
    
    # PERFORMANCE METRICS FRAME    
    tk.Label(ver_frame, text="RESULTING PERFORMANCE METRICS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=6)
    # Create Performance Metrics Text Box Labels
    tk.Label(ver_frame, text="Vdsat").grid(row=7, column=0, sticky=tk.E)
    tk.Label(ver_frame, text="gm").grid(row=8, column=0, sticky=tk.E)
    tk.Label(ver_frame, text="gmb").grid(row=9, column=0, sticky=tk.E)
    tk.Label(ver_frame, text="rds").grid(row=10, column=0, sticky=tk.E)
    tk.Label(ver_frame, text="Id").grid(row=11, column=0, sticky=tk.E)
    # Create Performance Metrics Text Boxes    
    global ver_Vdsat
    global ver_gm
    global ver_gmb
    global ver_rds
    global ver_Id
    ver_Vdsat = tk.Entry(ver_frame, width=30)
    ver_Vdsat.grid(row=7, column=1, padx=20)
    ver_gm = tk.Entry(ver_frame, width=30)
    ver_gm.grid(row=8, column=1, padx=20)
    ver_gmb = tk.Entry(ver_frame, width=30)
    ver_gmb.grid(row=9, column=1, padx=20)
    ver_rds = tk.Entry(ver_frame, width=30)
    ver_rds.grid(row=10, column=1, padx=20)
    ver_Id = tk.Entry(ver_frame, width=30)
    ver_Id.grid(row=11, column=1, padx=20)   
    # Create Units and Examples
    tk.Label(ver_frame, text="(V)").grid(row=7, column=2, sticky=tk.W)
    tk.Label(ver_frame, text="(mA/V)").grid(row=8, column=2, sticky=tk.W)
    tk.Label(ver_frame, text="(mA/V)").grid(row=9, column=2, sticky=tk.W)
    tk.Label(ver_frame, text="(k\u03A9)").grid(row=10, column=2, sticky=tk.W)
    tk.Label(ver_frame, text="(\N{MICRO SIGN}A)").grid(row=11, column=2, sticky=tk.W)

# Edit root to be open and function.
def database_edit():
        try:
             record_id = database_select_box.get()
             # Create a database or connect to one
             conn = sqlite3.connect(database_path)
             # Create cursor
             c = conn.cursor()    
             
             # Query the database
             c.execute("SELECT * FROM inputs WHERE oid = " + record_id)
             records = c.fetchall() 
                     
             global edt_root
             edt_root = tk.Tk()
             edt_root.title("Update TSMC Record " + record_id)
             edt_root.iconbitmap(icon_path)
             edt_root.geometry("520x755")   
             start_gui.center(edt_root)
        
             """
             ###########################
             # CREATE DATA INPUT FRAME #
             ###########################
             """
             global edt_frame
             edt_frame = tk.LabelFrame(edt_root, padx=30, pady=16, bd = 1, labelanchor = 'n', font = "none 15 bold")
             edt_frame.grid(column=0, row=0, padx=10, pady=20) 
             
             # DATABASE NAME FRAME
             tk.Label(edt_frame, text="DATABASE NAME", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=0)
             # Create Database text box label
             tk.Label(edt_frame, text="Declare a name").grid(row=1, column=0, pady=(20,0), sticky=tk.E)
             # Create Database Text Box
             global edt_database_name
             edt_database_name = tk.Entry(edt_frame, width=30)
             edt_database_name.grid(row=1, column=1, padx=20)
             # Create empty line
             tk.Label(edt_frame, text=" ").grid(column=1, row=2)
             
             
             
             # APPLICATION SPESIFICS FRAME
             tk.Label(edt_frame, text="APPLICATION SPESIFICS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=3)
             # Create Application Spesifics Text Box Labels
             tk.Label(edt_frame, text="Model deck").grid(row=4, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type .model").grid(row=5, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type Ldr(min)").grid(row=6, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type Wdr(min)").grid(row=7, column=0, sticky=tk.E)
             # Create Application Spesifics Text Boxes
             global edt_model_deck
             global edt_model
             global edt_Ldrmin
             global edt_Wdrmin
             edt_model_deck = tk.Entry(edt_frame, width=30)
             edt_model_deck.grid(row=4, column=1, padx=20)
             edt_model_deck.insert(0, "Locate a TSMC model deck file.")
             edt_model_deck.configure(state= tk.DISABLED)
             edt_model = tk.Entry(edt_frame, width=30)
             edt_model.grid(row=5, column=1, padx=20)
             edt_Ldrmin = tk.Entry(edt_frame, width=30)
             edt_Ldrmin.grid(row=6, column=1, padx=20) 
             edt_Wdrmin = tk.Entry(edt_frame, width=30)
             edt_Wdrmin.grid(row=7, column=1, padx=20) 
             # Create Units and Examples
             global open_btn
             img = Image.open(open_icon_path)
             resizedImage = img.resize((25, 25), Image.ANTIALIAS)
             open_btn = ImageTk.PhotoImage(resizedImage, master=edt_root)
             tk.Button(edt_frame, image=open_btn, command=open_file_edit, borderwidth=0).grid(row=4, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(ex: cmosn)").grid(row=5, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(\N{MICRO SIGN}m)").grid(row=6, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(\N{MICRO SIGN}m)").grid(row=7, column=2, sticky=tk.W)
             tk.Label(edt_frame, text=" ").grid(column=1, row=8)
             
             # PERFORMANCE METRICS FRAME    
             tk.Label(edt_frame, text="PERFORMANCE METRICS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=9)
             # Create Performance Metrics Text Box Labels
             tk.Label(edt_frame, text="Type Vdsat").grid(row=10, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type gm").grid(row=11, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type gmb").grid(row=12, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type rds").grid(row=13, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type Id").grid(row=14, column=0, sticky=tk.E)
             # Create Performance Metrics Text Boxes    
             global edt_Vdsat
             global edt_gm
             global edt_gmb
             global edt_rds
             global edt_Id
             edt_Vdsat = tk.Entry(edt_frame, width=30)
             edt_Vdsat.grid(row=10, column=1, padx=20)
             edt_gm = tk.Entry(edt_frame, width=30)
             edt_gm.grid(row=11, column=1, padx=20)
             edt_gmb = tk.Entry(edt_frame, width=30)
             edt_gmb.grid(row=12, column=1, padx=20)
             edt_rds = tk.Entry(edt_frame, width=30)
             edt_rds.grid(row=13, column=1, padx=20)
             edt_Id = tk.Entry(edt_frame, width=30)
             edt_Id.grid(row=14, column=1, padx=20)   
             # Create Units and Examples
             tk.Label(edt_frame, text="(V)").grid(row=10, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(mA/V)").grid(row=11, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(mA/V)").grid(row=12, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(k\u03A9)").grid(row=13, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(\N{MICRO SIGN}A)").grid(row=14, column=2, sticky=tk.W)
             tk.Label(edt_frame, text=" ").grid(column=1, row=15)
             
         
             # BIAS VOLTAGES FRAME
             tk.Label(edt_frame, text="EXTERNALLY IMPOSED BIAS VOLTAGES", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=16)
             # Create Bias Voltages Text Box Labels
             tk.Label(edt_frame, text="Type Vsb").grid(row=17, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type Vds").grid(row=18, column=0, sticky=tk.E)
             tk.Label(edt_frame, text="Type Vgs").grid(row=19, column=0, sticky=tk.E)
             # Create Bias Voltages Text Boxes 
             global edt_Vsb
             global edt_Vds
             global edt_Vgs
             edt_Vsb = tk.Entry(edt_frame, width=30)
             edt_Vsb.grid(row=17, column=1, padx=20)
             edt_Vds = tk.Entry(edt_frame, width=30) 
             edt_Vds.grid(row=18, column=1, padx=20)
             edt_Vgs = tk.Entry(edt_frame, width=30) 
             edt_Vgs.grid(row=19, column=1, padx=20)
             # Create Units and Examples
             tk.Label(edt_frame, text="(V)").grid(row=17, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(V)").grid(row=18, column=2, sticky=tk.W)
             tk.Label(edt_frame, text="(V)").grid(row=19, column=2, sticky=tk.W)
             tk.Label(edt_frame, text=" ").grid(column=1, row=20)
             
            # INITIAL GUESS FRAME    
             tk.Label(edt_frame, text="INITIAL GUESS", bd = 2, font = "none 9 bold", anchor=tk.S, padx=20, pady=5).grid(column=1, row=21)
             # Create Initial Guess Text Box Labels
             tk.Label(edt_frame, text="Type Initial Ldr").grid(row=22, column=0, sticky=tk.E)
             # Create Initial Guess Text Boxes 
             global edt_Ldr
             edt_Ldr = tk.Entry(edt_frame, width=30)
             edt_Ldr.grid(row=22, column=1, padx=20)
             # Create Units and Examples
             tk.Label(edt_frame, text="(\N{MICRO SIGN}m)").grid(row=22, column=2, sticky=tk.W)
             
             # INPUT BUTTONS
             # Create Info Button
             tk.Button(edt_frame, text="Information", command=info_button).grid(row=23, column=0, columnspan=3, pady=6, padx=10, ipadx=144)
             # Create Check Errors Button
             tk.Button(edt_frame, text="Check", command=error_checker_edt).grid(row=25, column=0, columnspan=3, pady=6, padx=10, ipadx=159)
         
             # Loop through results
             for record in records:
                edt_database_name.insert(0, record[0])
                
                edt_model_deck.configure(state= tk.NORMAL) 
                edt_model_deck.delete(0, tk.END)
                edt_model_deck.insert(0, record[1])
                edt_model_deck.configure(state= tk.DISABLED)  
                edt_model.insert(0, record[2])
                edt_Ldrmin.insert(0, record[3])
                edt_Wdrmin.insert(0, record[4])
                 
                 
                if record[5] != 0 :
                    edt_Vdsat.insert(0, record[5])
                if record[6] != 0 :
                    edt_gm.insert(0, record[6])
                if record[7] != 0 :
                    edt_gmb.insert(0, record[7])
                if record[8] != 0 :
                    edt_rds.insert(0, record[8])
                if record[9] != 0 :
                    edt_Id.insert(0, record[9])
                
                if record[10] != 0 :
                    edt_Vsb.insert(0, record[10])
                if record[11] != 0 :
                    edt_Vds.insert(0, record[11])
                if record[12] != 0 :
                    edt_Vgs.insert(0, record[12])
                    
                
                edt_Ldr.insert(0, record[13])
            
                         
             # Create a Save Button
             tk.Button(edt_root, text="Update Record", command=database_update).grid(row=1, column=0, columnspan=3, ipady=12, padx=10, ipadx=138)
            
        except:
            messagebox.showwarning("Warning", "Select a valid record ID.")


""" ENRTY BOX CONFIGURATIONS """
# Clear the Text Boxes in Simulation interface.
def clear_inp_boxes():
    database_name.delete(0, tk.END)
    inp_model_deck.configure(state= tk.NORMAL) 
    inp_model_deck.delete(0, tk.END)
    inp_model_deck.insert(0, "Locate a TSMC model deck file.")
    inp_model_deck.configure(state= tk.DISABLED) 
    inp_model.delete(0, tk.END)
    inp_Ldrmin.delete(0, tk.END)
    inp_Wdrmin.delete(0, tk.END)
    inp_Vdsat.delete(0, tk.END)
    inp_gm.delete(0, tk.END)
    inp_gmb.delete(0, tk.END)
    inp_rds.delete(0, tk.END)
    inp_Id.delete(0, tk.END)
    inp_Vsb.delete(0, tk.END)
    inp_Vds.delete(0, tk.END)
    inp_Vgs.delete(0, tk.END)
    inp_Ldr.delete(0, tk.END)

# Clear all the entry boxes
def clear_boxes():
    database_name.delete(0, tk.END)
    database_select_box.delete(0, tk.END)
    inp_model_deck.configure(state= tk.NORMAL) 
    inp_model_deck.delete(0, tk.END)
    inp_model_deck.insert(0, "Locate a TSMC model deck file.")
    inp_model_deck.configure(state= tk.DISABLED) 
    inp_model.delete(0, tk.END)
    inp_Ldrmin.delete(0, tk.END)
    inp_Wdrmin.delete(0, tk.END)
    inp_Vdsat.delete(0, tk.END)
    inp_gm.delete(0, tk.END)
    inp_gmb.delete(0, tk.END)
    inp_rds.delete(0, tk.END)
    inp_Id.delete(0, tk.END)
    inp_Vsb.delete(0, tk.END)
    inp_Vds.delete(0, tk.END)
    inp_Vgs.delete(0, tk.END)
    inp_Ldr.delete(0, tk.END)
    
# Clear the Text Boxes Simulation interface.
def clear_out_boxes():
    out_LINT.delete(0, tk.END)
    out_WINT.delete(0, tk.END)
    out_XL.delete(0, tk.END)
    out_XW.delete(0, tk.END)
    out_Ldr.delete(0, tk.END)
    out_Wdr.delete(0, tk.END)
    out_Vsb.delete(0, tk.END)
    out_Vds.delete(0, tk.END)
    out_Vgs.delete(0, tk.END)   

# Enable or disable entry boxes.
def enable_out_boxes():
    out_LINT.configure(state = tk.NORMAL)
    out_WINT.configure(state = tk.NORMAL)
    out_XL.configure(state = tk.NORMAL)
    out_XW.configure(state = tk.NORMAL)
    out_Ldr.configure(state = tk.NORMAL)
    out_Wdr.configure(state = tk.NORMAL)
    out_Vsb.configure(state = tk.NORMAL)
    out_Vds.configure(state = tk.NORMAL)
    out_Vgs.configure(state = tk.NORMAL)
def disable_out_boxes():
    out_LINT.configure(state = tk.DISABLED)
    out_WINT.configure(state = tk.DISABLED)
    out_XL.configure(state = tk.DISABLED)
    out_XW.configure(state = tk.DISABLED)
    out_Ldr.configure(state = tk.DISABLED)
    out_Wdr.configure(state = tk.DISABLED)
    out_Vsb.configure(state = tk.DISABLED)
    out_Vds.configure(state = tk.DISABLED)
    out_Vgs.configure(state = tk.DISABLED)    
def enable_ver_boxes():
    ver_Vdsat.configure(state = tk.NORMAL)
    ver_gm.configure(state = tk.NORMAL)
    ver_gmb.configure(state = tk.NORMAL)
    ver_rds.configure(state = tk.NORMAL)
    ver_Id.configure(state = tk.NORMAL)
def disable_ver_boxes():
    ver_Vdsat.configure(state = tk.DISABLED)
    ver_gm.configure(state = tk.DISABLED)
    ver_gmb.configure(state = tk.DISABLED)
    ver_rds.configure(state = tk.DISABLED)
    ver_Id.configure(state = tk.DISABLED)



""" DATABASE """
# Search and place the saved data from selected database ID.
def database_query():
    # Create a database or connect to one
    conn = sqlite3.connect(Database_File)
    # Create cursor
    c = conn.cursor()    
    # Query the database
    c.execute("SELECT *, oid FROM inputs")
    records = c.fetchall()
        
    # Loop Through Results
    print_records=''
    for record in records:
        print_records += str(record[14]) + "  :  " + str(record[0]) + "\n"
    
    global show_records
    show_records = tk.Tk()
    show_records.title("Database Records")
    show_records.iconbitmap(icon_path)
    show_records.geometry("350x350") 
    start_gui.center(show_records)
    
    tk.Label(show_records, text=print_records, justify=tk.LEFT).place(relx = 0.5,
                   rely = 0.5,
                   anchor = 'center')
    
    ttk.Scrollbar(show_records, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y)
    
    # Comit Changes
    conn.commit()
    # Close Connection
    conn.close()    
    return  

# Get Input Values to program variables.
def database_get_inp():
    
    # Create a database or connect to one
    conn = sqlite3.connect(database_path)
    # Create cursor
    c = conn.cursor()    
    if(database_select_box.get()):
        record_id = database_select_box.get()
        # Query the database
        c.execute("SELECT * FROM inputs WHERE oid = " + record_id)
        records = c.fetchall()
        clear_inp_boxes()
        for record in records:
            database_name.insert(0, record[0])
            inp_model_deck.configure(state= tk.NORMAL)  
            inp_model_deck.delete(0, tk.END)
            inp_model_deck.insert(0, record[1])
            inp_model_deck.configure(state= tk.DISABLED)  
            inp_model.insert(0, record[2])
            inp_Ldrmin.insert(0, record[3])
            inp_Wdrmin.insert(0, record[4])
            
            if record[5] != 0 :
                inp_Vdsat.insert(0, record[5])
            if record[6] != 0 :
                inp_gm.insert(0, record[6])
            if record[7] != 0 :
                inp_gmb.insert(0, record[7])
            if record[8] != 0 :
                inp_rds.insert(0, record[8])
            if record[9] != 0 :
                inp_Id.insert(0, record[9])
            
            if record[10] != 0 :
                inp_Vsb.insert(0, record[10])
            if record[11] != 0 :
                inp_Vds.insert(0, record[11])
            if record[12] != 0 :
                inp_Vgs.insert(0, record[12])

            
            inp_Ldr.insert(0, record[13])
    else:
        messagebox.showwarning("Warning", "Select a valid record ID")
    
# Create function to submit inputs.
def database_submit_inp():
    
    # Create a database or connect to one
    conn = sqlite3.connect(Database_File)
    # Create cursor
    c = conn.cursor()
    
    # Insert Into Table
    c.execute("INSERT INTO inputs VALUES (:database_name, :model_deck, \
                  :model, :Ldrmin, :Wdrmin, :Vdsat, :gm, \
                  :gmb, :rds, :Id,  :Vsb, :Vds, :Vgs, :Ldr)",
              {
                  'database_name': database_name.get(),
                  'model_deck': inp_model_deck.get(),
                  'model': inp_model.get(),
                  'Ldrmin': inp_Ldrmin.get(),
                  'Wdrmin': inp_Wdrmin.get(),
                  'Vdsat': inp_Vdsat.get(),
                  'gm': inp_gm.get(),
                  'gmb': inp_gmb.get(),
                  'rds': inp_rds.get(),
                  'Id': inp_Id.get(),
                  'Vsb': inp_Vsb.get(),
                  'Vds': inp_Vds.get(),
                  'Vgs': inp_Vgs.get(),
                  'Ldr': inp_Ldr.get()
              })    
    # Comit Changes
    conn.commit()
    # Close Connection
    conn.close()
    
    messagebox.showinfo("Info", "All input data have been succesfully added to a new database record.")

# Create function to delete a record.
def database_delete():
    # Create a database or connect to one
    conn = sqlite3.connect(Database_File)
    # Create cursor
    c = conn.cursor()

    #DeLete a record
    if(database_select_box.get()):
        if (areyousure()):
            c.execute("DELETE from inputs WHERE oid= " + database_select_box.get())
            clear_boxes()
            messagebox.showinfo("Info", "Selected Record has been successfully deleted.")
    else:
        messagebox.showwarning("Warning", "Select a valid record ID.")

    
    # Comit Changes
    conn.commit()
    # Close Connection
    conn.close()        
    
# Update or edit an input record saved in to the database file.
def database_update():
    # Create a database or connect to one
    conn = sqlite3.connect(database_path)
    # Create cursor
    c = conn.cursor()  
    
    record_id = database_select_box.get()
    c.execute(""" UPDATE inputs SET
            database_name = :database_name,
            model_deck = :model_deck,
            model = :model,
            Ldrmin = :Ldrmin,
            Wdrmin = :Wdrmin,
            Vdsat = :Vdsat,
            gm = :gm,
            gmb = :gmb,
            rds = :rds,
            Id = :Id,
            Vsb = :Vsb,
            Vds = :Vds,
            Vgs = :Vgs,
            Ldr = :Ldr
            
            WHERE oid = :oid""",
            {
            'database_name': edt_database_name.get(),
            'model_deck' : edt_model_deck.get(),
            'model' : edt_model.get(),
            'Ldrmin' : edt_Ldrmin.get(), 
            'Wdrmin' : edt_Wdrmin.get(),
            'Vdsat' : edt_Vdsat.get(),
            'gm' : edt_gm.get(),
            'gmb' : edt_gmb.get(),
            'rds' : edt_rds.get(),
            'Id' : edt_Id.get(),
            'Vsb' : edt_Vsb.get(),
            'Vds' : edt_Vds.get(),
            'Vgs' : edt_Vgs.get(),
            'Ldr' : edt_Ldr.get(),

            'oid' : record_id              
            })             
    
    # Comit Changes
    conn.commit()
    # Close Connection
    conn.close()  
    edt_root.destroy()
    
    messagebox.showinfo("Info", "Database record succesfully updated.")
    
    
    
""" SIMULATION """
# Check input values if any errors.
def error_checker_inp():
    try:
        model_deck = inp_model_deck.get()
        if ((model_deck != "") or (model_deck != "Locate a TSMC model deck file.")):
            try:
                model = inp_model.get()
                try:
                    Ldrmin = float(inp_Ldrmin.get())
                except:
                    Ldrmin = 0    
                try:
                    Wdrmin = float(inp_Wdrmin.get())
                except:
                    Wdrmin = 0
                try:
                    Vdsat = float(inp_Vdsat.get())
                except:
                    Vdsat = 0
                try:
                    gm = float(inp_gm.get())
                except:
                    gm = 0
                try:
                    gmb = float(inp_gmb.get())
                except:
                    gmb = 0
                try:
                    rds = float(inp_rds.get())
                except:
                    rds = 0    
                try:
                    Id = float(inp_Id.get())
                except:
                    Id = 0
                try:
                    Vsb = float(inp_Vsb.get())
                except:
                    Vsb = 0
                try:
                    Vds = float(inp_Vds.get())
                except:
                    Vds = 0
                try:
                    Vgs = float(inp_Vgs.get())
                except:
                    Vgs = 0
                try:
                    Ldr = float(inp_Ldr.get())
                except:
                    Ldr = 0
            except: 
                messagebox.showwarning("Warning", "Please type a model name.")
        else:
            messagebox.showwarning("Warning", "Please choose a model deck file.")
    finally :    
       return error_checker(model_deck, model, Ldrmin, Wdrmin, Vdsat, gm, gmb, rds, Id, Vsb, Vds, Vgs, Ldr, sim_option_speed)       
def error_checker_edt():
    try:
        model_deck = inp_model_deck.get()
        if ((model_deck != "") or (model_deck != "Locate a TSMC model deck file.")):
            try:
                model = edt_model.get()
                try:
                    Ldrmin = float(edt_Ldrmin.get())
                except:
                    Ldrmin = 0    
                try:
                    Wdrmin = float(edt_Wdrmin.get())
                except:
                    Wdrmin = 0
                try:
                    Vdsat = float(edt_Vdsat.get())
                except:
                    Vdsat = 0
                try:
                    gm = float(edt_gm.get())
                except:
                    gm = 0
                try:
                    gmb = float(edt_gmb.get())
                except:
                    gmb = 0
                try:
                    rds = float(edt_rds.get())
                except:
                    rds = 0    
                try:
                    Id = float(edt_Id.get())
                except:
                    Id = 0
                try:
                    Vsb = float(edt_Vsb.get())
                except:
                    Vsb = 0
                try:
                    Vds = float(edt_Vds.get())
                except:
                    Vds = 0
                try:
                    Vgs = float(edt_Vgs.get())
                except:
                    Vgs = 0
                try:
                    Ldr = float(edt_Ldr.get())
                except:
                    Ldr = 0
            except: 
                messagebox.showwarning("Warning", "Please type a model name.")
        else:
            messagebox.showwarning("Warning", "Please choose a model deck file.")
    except: 
        messagebox.showwarning("Warning", "Please type a model deck file.")
    finally :    
        error_checker(model_deck, model, Ldrmin, Wdrmin, Vdsat, gm, gmb, rds, Id, Vsb, Vds, Vgs, Ldr, sim_option_speed)
def error_checker(model_deck, model, Ldrmin, Wdrmin, Vdsat, gm, gmb, rds, Id, Vsb, Vds, Vgs, Ldr, sim_option_speed):
    error_count = 0
    error_message = ''
    global iter_speed
    iter_speed = ng.define_speed_var(sim_option_speed)
    try :
        # Check if model_deck file exists
        with open(model_deck, 'r') as fh:
            data_raw = fh.read().rstrip().split("*")
            while("" in data_raw) :
                data_raw.remove("")
        for x in range(0, len(data_raw)) :
            data_raw[x] = data_raw[x].split("(")
            data_raw[x] = data_raw[x][0]
            data_raw[x] = data_raw[x].split(".MODEL")
            data_raw[x] = data_raw[x][1]
            data_raw[x] = data_raw[x].split(" ")
            while("" in data_raw[x]) :
                data_raw[x].remove("")
        model = model.upper()
        if(not (((data_raw[0][0] == model) or (data_raw[0][1] == model)) or ((data_raw[1][0] == model) or (data_raw[1][1] == model)))) :
            error_count += 1
            error_message += "\nName Error : Model deck does not contain model name.\n"
        else:
            
            # Check Wdrmin and Ldrmin    
            if (Wdrmin <= 0):
                error_count += 1
                error_message += "\nValue Error : Wdrmin can not be negative or zero.\n"
            if (Ldrmin <= 0):
                error_count += 1
                error_message += "\nValue Error : Ldrmin can not be negative or zero.\n" 
                      
            # Check if rds and Vds matches
            if (((rds > 0) and (Vds == 0)) or  ((rds == 0) and (Vds > 0))):
                error_count += 1
                error_message += "\nValue Error : rds changes with Vds bias voltage. rds must be defined together with Vds.\n"
                     
            # Check if gm and gmb defined together
            if (not ((((gm >= 0) or (gm <= 0)) and (gmb == 0)) or ((gm == 0) and ((gmb >= 0) or (gmb <= 0)))) ):
                error_count += 1
                error_message += "\nOverconstraint Error : gm and gmb can not be defined at the same time.\n"      
                   
            MOS = ng_func.whichMOS(model_deck, model, 1)     
            if (MOS == 1) :
                if (Vds < 0) :
                    error_count += 1
                    error_message += "\nValue Error : Vds has to be positive  for an NMOS device\n"
            elif ((MOS == 0)) :
                if (Vds > 0) :
                    error_count += 1
                    error_message += "\nValue Error : Vds has to be negative for a PMOS device\n"
                    
            
            
            error_number = ng_func.check_constraints(Vdsat, gm, gmb, Id)
            if (error_number == 1):
                error_count += 1
                error_message += "\nOverconstraint Error : Id, Vdsat and (gm or gmb) can not be defined at the same time.\n"
            elif (error_number == 2):
                error_count += 1
                error_message += "\nUnderconstraint Error : Id or Vdsat have to be defined.\n"
            elif (error_number == 3):
                error_count += 1
                error_message += "\nUnderconstraint Error : Id or (gm or gmb) have to be defined.\n"
            elif (error_number == 4):
                error_count += 1
                error_message += "\nUnderconstraint Error : Vdsat or (gm or gmb) have to be defined.\n"
        
        
            if (Ldr < Ldrmin):
                error_count += 1
                error_message += "\nValue Error : Initial Ldr can not be smaller then Ldrmin."
                
        if (error_count == 0):  
            messagebox.showinfo("Error Checker", "Error Check Completed. No errors have been found.")
            return 1
        else :
            messagebox.showwarning("\nError Checker", error_message)   
            return 0
        
    except :
        messagebox.showwarning("Warning", "\nFile Error : Model deck does not exist.\n")
        error_count += 1

    
# Use vds and vsb while extracting raw_data from figures.
def options():
    global opt_root
    opt_root = tk.Tk()
    opt_root.title("Simulation Options")
    opt_root.iconbitmap(icon_path)
    opt_root.geometry("313x290")   
    opt_root.configure(background='white')
    start_gui.center(opt_root)
    
    
    opt_frame = tk.LabelFrame(opt_root, padx=30, pady=16, bd = 1, labelanchor = 'n', font = "none 15 bold", background='white')
    opt_frame.grid(column=0, row=0, padx=10, pady=50, columnspan=2) 

    # SELECT MODEL DECK
    global options
    global options_combo
    options = [
    "Use Vds and Vsb",
    "Use Vds",
    "Use Vsb",
    "Do not use any"
    ]
    
    tk.Label(opt_frame, text="Please select an option.", background='white').grid(row=0,column=0)
    options_combo = ttk.Combobox(opt_frame,value=options, background='white')
    options_combo.current(0)
    options_combo.grid(row=1, column=0, columnspan=2, pady=6, padx=10, ipadx=10)
    
    
    # SELECT SIMULATION SPEED
    global speed_options
    global speed_options_combo
    speed_options = [
    "Faster",
    "Fast",
    "Slow",
    "Slower"
    ]
    
    tk.Label(opt_frame, text="Please select a speed.", background='white').grid(row=2,column=0)
    speed_options_combo = ttk.Combobox(opt_frame,value=speed_options, background='white')
    speed_options_combo.current(0)
    speed_options_combo.grid(row=3, column=0, columnspan=2, pady=6, padx=10, ipadx=10)
    
        
    tk.Button(opt_root, text="Save", command=chose_option).grid(row=1, column=0, pady=2, padx=10, ipadx=50)
    tk.Button(opt_root, text="Quit", command=opt_root.destroy).grid(row=1, column=1, pady=2, padx=10, ipadx=50)      
def chose_option():
    global sim_option
    if(options_combo.get() == options[0]):
        messagebox.showinfo("Info", "You have choosed to use Vds and Vsb in simulation.")
        sim_option = 0
    elif(options_combo.get() == options[1]):
        messagebox.showinfo("Info", "You have choosed to use Vds in simulation.")
        sim_option = 1
    elif(options_combo.get() == options[2]):
        messagebox.showinfo("Info", "You have choosed to use Vsb in simulation.")
        sim_option = 2
    elif(options_combo.get() == options[3]):
        messagebox.showinfo("Info", "You have choosed not to use any in simulation.")
        sim_option = 3
        
    global sim_option_speed
    if(speed_options_combo.get() == speed_options[0]):
        messagebox.showinfo("Info", "Faster - Please choose a lower option if the simulation fails.")
        sim_option_speed = 0
    elif(speed_options_combo.get() == speed_options[1]):
        messagebox.showinfo("Info", "Fast - Please choose a lower option if the simulation fails.")
        sim_option_speed = 1
    elif(speed_options_combo.get() == speed_options[2]):
        messagebox.showinfo("Info", "Slow - Please choose a lower option if the simulation fails.")
        sim_option_speed = 2
    elif(speed_options_combo.get() == speed_options[3]):
        messagebox.showinfo("Info", "Slower - Please upgrade your system performance if the simulation fails.")
        sim_option_speed = 3

# Verify the results.
def verification():
        try :
            enable_out_boxes()
            Ldr_res =  float(out_Ldr.get())
            Wdr_res =  float(out_Wdr.get())
            Vsb_res =  float(out_Vsb.get())
            Vds_res =  float(out_Vds.get())
            Vgs_res =  float(out_Vgs.get())
            disable_out_boxes()
            try:
                if (Vgs_res < 0):
                    MOS = 0
                    Vdsat, Id, gm, gmb, rds = ng_base.sort_results(p_verify_txt_path, MOS, model_deck, Wdr_res, Ldr_res, Vgs_res, Vds_res, Vsb_res, iter_speed)
                    Vdsat = -Vdsat
            
                else:
                    MOS = 1
                    Vdsat, Id, gm, gmb, rds = ng_base.sort_results(n_verify_txt_path, MOS, model_deck, Wdr_res, Ldr_res, Vgs_res, Vds_res, Vsb_res, iter_speed)
                
                Id = Id*1000000
                gm = gm*1000
                gmb = gmb*1000
                rds = rds/1000
                    
                initialize_verification()
                enable_ver_boxes()
                ver_Vdsat.insert(0, "{:.3f}".format(Vdsat))
                ver_gm.insert(0, "{:.3f}".format(gm))
                ver_gmb.insert(0, "{:.3f}".format(gmb))
                ver_rds.insert(0, "{:.3f}".format(rds))
                ver_Id.insert(0, "{:.3f}".format(Id))
                disable_ver_boxes()
            except:
                messagebox.showerror("Error", "An error occured during verification!")
        except:
            disable_out_boxes()
            messagebox.showwarning("Warning", "Please run a simulation first.")


    
 
# Simulate Figure 3.24 according to given inputs and show outputs in GUI
def simulate():
    enable_out_boxes()
    clear_out_boxes()
    disable_out_boxes()
    
    try:
        global model_deck
        model_deck = inp_model_deck.get()
        model = inp_model.get()
        try:
            Ldrmin = float(inp_Ldrmin.get())
        except:
            Ldrmin = 0    
        try:
            Wdrmin = float(inp_Wdrmin.get())
        except:
            Wdrmin = 0
        try:
            Vdsat = float(inp_Vdsat.get())
        except:
            Vdsat = 0
        try:
            gm = float(inp_gm.get())
            gm = gm/1000
        except:
            gm = 0
        try:
            gmb = float(inp_gmb.get())
            gmb = gmb/1000
        except:
            gmb = 0
        try:
            rds = float(inp_rds.get())
            rds = rds*1000
        except:
            rds = 0    
        try:
            Id = float(inp_Id.get())
            Id = Id/1000000
        except:
            Id = 0
        try:
            Vsb = float(inp_Vsb.get())
        except:
            Vsb = 0
        try:
            Vds = float(inp_Vds.get())
        except:
            Vds = 0
        try:
            Vgs = float(inp_Vgs.get())
        except:
            Vgs = 0
        try:
            Ldr = float(inp_Ldr.get())
        except:
            Ldr = 0
    except:
        messagebox.showerror("Error", "An error occured during extracting input data! Please run again.")                    
    finally:
        if(error_checker_inp()):
            try: 
                
                shutil.copy2(model_deck, raw_data_path)
 
                LINT, WINT, XL, XW, \
                    Ldr, Wdr, Vsb, Vds, Vgs \
                        = ng.simulate (sim_option_speed, sim_option,\
                (model_deck.split("/")[-1]), model, Wdrmin, Ldrmin, Vdsat, gm, \
                gmb, rds, Id, Vsb, Vds, Vgs, Ldr )
                            
                os.remove(raw_data_path + (model_deck.split("/")[-1]))
                
                enable_out_boxes()
                
                out_LINT.insert(0, str(LINT).upper())
                out_WINT.insert(0, str(WINT).upper())
                out_XL.insert(0, str(XL).upper())
                out_XW.insert(0, str(XW).upper())
                out_Ldr.insert(0, "{:.2f}".format(Ldr))
                out_Wdr.insert(0, "{:.2f}".format(Wdr))
                out_Vsb.insert(0, "{:.3f}".format(Vsb))
                out_Vds.insert(0, "{:.3f}".format(Vds))
                out_Vgs.insert(0, "{:.3f}".format(Vgs))
            
                disable_out_boxes()
                
                messagebox.showinfo("Info", "Simulation has been succesfully completed.")     
            except:
                messagebox.showerror("Error", "An error occured during simulation! Please run again.")
            
            
            
            
""" RUN WHEN THE LIBRARY IS CALLED """            
define_global_paths()
    
    


