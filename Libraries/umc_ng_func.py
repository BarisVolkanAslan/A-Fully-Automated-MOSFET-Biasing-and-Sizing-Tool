"""  MOSFET Biasing and Sizing Tool Library

This library allows a user to acces Ngspice simulation platform from Python.
By this way design process can be automated.

[1] Cilingiroglu, Ugur (2019) ‘Analog Integrated Design by Simulation: 
    Techniques, Tools, and Methods’, McGraw-Hill Education.

Created by:
    Baris Volkan ASLAN
    Microelectronics Laboratory
    Electrical and Electronics Eng. Dept.
    Yeditepe University
    Istanbul / TURKEY
"""
import os
import numpy as np
import matplotlib.pyplot as plt



"""  Define the type of MOSFET device being simulated.
If returned 0 it is a PMOS device
If return 1 it is an NMOS device
10/04/21
"""
def bsim_whichMOS(model_deck, model_name):
    model_name = model_name.upper()
    with open(raw_data_path + model_deck, 'r') as fh:
        data_raw = fh.read().rstrip().split("*")
        while("" in data_raw) :
            data_raw.remove("")
        
    for x in range(0, len(data_raw)) :
        data_raw[x] = data_raw[x].split("(")
        
    x = data_raw[0][0].find(model_name)
    if(x<0) :
        return 0 #PMOS
    else:
        return 1 #NMOS



"""  Under or over constraint check."""    
def check_constraints(Vdsat, gm, gmb, Id):
    if ((Id != 0) and (Vdsat != 0) and ((gm != 0) or (gmb !=0))):
        print("Overconstraint Error : Id, Vdsat and (gm or gmb) can not be defined at the same time.")
        return 1
    elif ( (Id == 0) and (Vdsat == 0) ):
        print("Underconstraint Error : Id or Vdsat have to be defined.")
        return 2
    elif ( ((gm == 0) and (gmb == 0)) and (Id == 0)):
        print("Underconstraint Error : Id or (gm or gmb) have to be defined.")
        return 3
    elif ( ((gm == 0) and (gmb == 0)) and (Vdsat == 0)):
        print("Underconstraint Error : Vdsat or (gm or gmb) have to be defined.")    
        return 4
    else :
        return 0


    
"""  Index of the closest value in an array pair.
Find the closest value in an array and return its index.
This method is being used to find the cross value
inside an output data.
08/03/2021
"""    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
   
"""  Decide the algorithm to be followed during simulation."""      
def which_case (Vdsat, rds, gm, gmb, Id):
    try:
        if ((Vdsat != 0) and (rds != 0) and ((gm != 0) or (gmb != 0))) :
            case = 1
        elif ((Id != 0) and (rds != 0) and ((gm != 0) or (gmb != 0))) :
            case = 2
        elif ((Id != 0) and (rds != 0) and (Vdsat != 0)) :
            case = 3        
        return case
    except ValueError:
        print("Error : Case")  

"""  Plot simulation results and save them in a file."""
def plot_lists(list_iteration, list_factor, list_Ldr, Va_tar, list_simVa, list_error):
        plt.figure(figsize =(10, 10)) 
          
        os.getcwd()
        
        sub1 = plt.subplot(2, 2, 1) 
        sub2 = plt.subplot(2, 2, 2) 
        sub3 = plt.subplot(2, 2, 3) 
        sub4 = plt.subplot(2, 2, 4) 
          
        sub1.plot(list_Ldr, color='b', linestyle='-', linewidth = 0.35,
             marker='.',mfc='b', label = "Drawn Channel Length (\N{MICRO SIGN}m)" )  
        sub1.set_xticks(list_iteration) 
        sub1.set_title('L(dr) vs Iteration')
        sub1.minorticks_on()
        sub1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        # sub1.set_xlabel('Iteration')
        sub1.set_ylabel("Meters ( \N{MICRO SIGN} )")
        sub1.legend()
        
        
        
        sub2.plot(list_simVa, color='b', linestyle='-', linewidth = 0.35,
             marker='.',mfc='b', label = "Simulated Early Voltage" ) 
        sub2.set_xticks(list_iteration) 
        sub2.set_title('Simulated V(a) vs Iteration')
        sub2.minorticks_on()
        sub2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        # sub2.set_xlabel('Iteration')
        sub2.set_ylabel('Voltage ( V )')
        sub2.legend()
        
        

        sub3.plot(list_error, color='b', linestyle='-', linewidth = 0.35,
             marker='.',mfc='b', label = "Error Percentage" ) 
        sub3.set_xticks(list_iteration) 
        sub3.set_title('Error vs Iteration')
        sub3.minorticks_on()
        sub3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        # sub3.set_xlabel('Iteration')
        sub3.set_ylabel('Percentage ( % )')
        sub3.legend()
        
    
        
        sub4.plot(list_factor, marker='.',mfc='b', linestyle='--', linewidth = 0.4)
        sub4.set_xticks(list_iteration)
        sub4.set_title('Factor vs Iteration')
        sub4.minorticks_on()
        sub4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        # sub4.set_xlabel('Iteration')
        sub4.set_ylabel('Factor')
        # sub4.legend() 
        
        
        plt.savefig(img_path, bbox_inches='tight', dpi=200)

"""  Remove the ngspice raw data files and netlists which were created during the simulation process."""
def remove(MOS) :
    if MOS == 1 :           
        os.remove("b3v32check.log")
        os.remove(raw_data_path + n_mos1_cir_path)
        os.remove(raw_data_path + n_Vdsat_Vov_txt_path)
        os.remove(raw_data_path + n_Ish_Vov_txt_path)
        os.remove(raw_data_path + n_gmId_Vov_txt_path)
        os.remove(raw_data_path + n_gmbId_Vov_txt_path)
        os.remove(raw_data_path + n_gmgmbId_Vov_txt_path)
        os.remove(raw_data_path + n_Va_cir_path)
        os.remove(raw_data_path + n_Va_txt_path)
        os.remove(raw_data_path + n_Vth_cir_path)
        os.remove(raw_data_path + n_Vth_txt_path)
    else :
        os.remove("b3v32check.log")
        os.remove(raw_data_path + p_mos1_cir_path)
        os.remove(raw_data_path + p_Vdsat_Vov_txt_path)
        os.remove(raw_data_path + p_Ish_Vov_txt_path)
        os.remove(raw_data_path + p_gmId_Vov_txt_path)
        os.remove(raw_data_path + p_gmbId_Vov_txt_path)
        os.remove(raw_data_path + p_gmgmbId_Vov_txt_path)
        os.remove(raw_data_path + p_Va_cir_path)
        os.remove(raw_data_path + p_Va_txt_path)
        os.remove(raw_data_path + p_Vth_cir_path)
        os.remove(raw_data_path + p_Vth_txt_path)         

"""  Define global path locations of txt files and netlists."""
def define_global_paths():
    global raw_data_path
    raw_data_path = "sim_data/BSIM/"
    
    global img_path
    img_path = "Images/UMC Simulations/simulation.png"
    
    global n_mos1_cir_path
    global n_Va_cir_path
    global n_Va_txt_path
    global n_Vth_cir_path
    global n_Vth_txt_path
    global n_Vdsat_Vov_txt_path
    global n_Ish_Vov_txt_path
    global n_gmId_Vov_txt_path
    global n_gmbId_Vov_txt_path
    global n_gmgmbId_Vov_txt_path
    global n_gmId_Vov_txt_path
    global n_gmbId_Vov_txt_path
    global n_gmgmbId_Vov_txt_path
    
    n_mos1_cir_path = 'n_mos1.cir'
    n_Va_cir_path = 'n_Va.cir'
    n_Va_txt_path = 'n_Va.txt'
    n_Vth_cir_path = 'n_Vth.cir'
    n_Vth_txt_path = 'n_Vth.txt'
    n_Vdsat_Vov_txt_path = 'n_Vdsat_Vov.txt'
    n_Ish_Vov_txt_path = 'n_Ish_Vov.txt'
    n_gmId_Vov_txt_path = 'n_gmId_Vov.txt'
    n_gmbId_Vov_txt_path = 'n_gmbId_Vov.txt'
    n_gmgmbId_Vov_txt_path = 'n_gmgmbId_Vov.txt'
    n_gmId_Vov_txt_path = 'n_gmId.txt'
    n_gmbId_Vov_txt_path = 'n_gmbId.txt'
    n_gmgmbId_Vov_txt_path = 'n_gmgmbId.txt'
    
    global p_mos1_cir_path
    global p_Va_cir_path
    global p_Va_txt_path
    global p_Vth_cir_path
    global p_Vth_txt_path
    global p_Vdsat_Vov_txt_path
    global p_Ish_Vov_txt_path
    global p_gmId_Vov_txt_path
    global p_gmbId_Vov_txt_path
    global p_gmgmbId_Vov_txt_path
    global p_gmId_Vov_txt_path
    global p_gmbId_Vov_txt_path
    global p_gmgmbId_Vov_txt_path
    
    p_mos1_cir_path = 'p_mos1.cir'
    p_Va_cir_path = 'p_Va.cir'
    p_Va_txt_path = 'p_Va.txt'
    p_Vth_cir_path = 'p_Vth.cir'
    p_Vth_txt_path = 'p_Vth.txt'
    p_Vdsat_Vov_txt_path = 'p_Vdsat_Vov.txt'
    p_Ish_Vov_txt_path = 'p_Ish_Vov.txt'
    p_gmId_Vov_txt_path = 'p_gmId_Vov.txt'
    p_gmbId_Vov_txt_path = 'p_gmbId_Vov.txt'
    p_gmgmbId_Vov_txt_path = 'p_gmgmbId_Vov.txt'
    p_gmId_Vov_txt_path = 'p_gmId.txt'
    p_gmbId_Vov_txt_path = 'p_gmbId.txt'
    p_gmgmbId_Vov_txt_path = 'p_gmgmbId.txt'        
        
define_global_paths()