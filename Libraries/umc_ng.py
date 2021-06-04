# -*- coding: utf-8 -*-
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

import sys
import os.path
libdir = os.path.dirname(__file__)
sys.path.append(os.path.split(libdir)[0])   
from Libraries import umc_ng_base
from Libraries import umc_ng_func
ngbase = umc_ng_base
ngfunc = umc_ng_func



def define_speed_var(sim_speed):
    global iter_speed
    if(sim_speed == 0):
        iter_speed = 0.3
    elif(sim_speed == 1):
        iter_speed = 0.4  
    elif(sim_speed == 2):
        iter_speed = 0.5    
    elif(sim_speed == 3):
        iter_speed = 1     
    return iter_speed



"""Call this function from umc_gui.py.
This function will start a UMC simulation.
Function inputs will be taken from input boxes of GUI,
Function outputs will be placed to empty boxes into output boxes of GUI.

10/04/2021
"""       
def simulate(sim_speed, sim_option, model_deck, model_lib, model_name, Vdsat, gm, \
    gmb, rds, Id, Vsb, Vds, Vgs, Ldr):
    
    Ldrmin = ngbase.extract_umc_param(model_deck, model_lib, model_name, "lmin")
    Wdrmin = ngbase.extract_umc_param(model_deck, model_lib, model_name, "wmin")
    Wdr = 20*Wdrmin
    model_desc = ngbase.extract_umc_param(model_deck, model_lib, model_name, "decription")
             
    MOS = ngfunc.umc_whichMOS(model_deck, model_lib, model_name)
    
    if(sim_option == 0):     
        Vov, W_L, Va_tar = flowchart(MOS, model_deck, Vdsat, rds, gm, gmb, Id, Vds, Vsb, iter_speed)
    elif(sim_option == 1):     
        Vov, W_L, Va_tar = flowchart(MOS, model_deck, Vdsat, rds, gm, gmb, Id, Vds, 0, iter_speed)
    elif(sim_option == 2):     
        Vov, W_L, Va_tar = flowchart(MOS, model_deck, Vdsat, rds, gm, gmb, Id, 0, Vsb, iter_speed)
    elif(sim_option == 3):     
        Vov, W_L, Va_tar = flowchart(MOS, model_deck, Vdsat, rds, gm, gmb, Id, 0, 0, iter_speed)     
        
    LINT, WINT, XL, XW, Wdr, Ldr, Vgs = iteration(sim_option, MOS, model_deck, model_lib, model_name, Wdr, Ldr, Vsb, Vds, Vov, Va_tar, W_L, Ldrmin, iter_speed)    
    
    ngfunc.remove(MOS)
    
    return  model_desc, LINT, WINT, XL, XW, Wdrmin, Ldrmin, Ldr, Wdr, Vsb, Vds, Vgs    
    
  
"""  Decide which case to follow during simulation.
There are three different cases in the flowchart to be followed.
Flowchart function decides to run the appropriate case.

10/04/2021
"""      
def flowchart(MOS, model_deck, Vdsat, rds, gm, gmb, Id):
    case = ngfunc.which_case(Vdsat, rds, gm, gmb, Id)
    if (case == 1):
        Vov, W_L, Va_tar = amplifier_driver_flowchart(MOS, model_deck, Vdsat, gm, gmb, rds)  
    elif (case == 2):
        Vov, W_L, Va_tar = current_source_sink_flowchart(MOS, model_deck, Vdsat, gm, gmb, rds)      
    elif (case == 3):
        Vov, W_L, Va_tar = unknown_flowchart(MOS, model_deck, Vdsat, Id, rds)
    return Vov, W_L, Va_tar

""""Iteration algorithm to find Ldr until reaching the target Va value."""
def iteration (MOS, model_deck, model_lib, model_name, Wdrmin, Ldr, Vsb, Vds, Vov, Va_tar, W_L):
    
    """  iteration for channel length  """
    Wdr = 20*Wdrmin
    itera = 0
    error = 0
    factor = 0
    list_error = []
    list_simVa = []
    list_Ldr = []
    list_Wdr = []
    list_Vgs = []
    list_Vth = []
    list_factor = []
    list_iteration = []

    Vth = get_Vth (MOS, model_deck, Wdr, Ldr, Vsb)
    Vgs = Vov + Vth                                               # find vgs by vth
    Va_sim = calc_Va_sim(MOS, model_deck, Vds, Vgs, Wdr, Ldr)
    error = calc_error(Va_sim, Va_tar)
    factor = find_factor(error)
    
    list_iteration.append(itera)
    list_factor.append(factor)
    list_Ldr.append(round(Ldr, 3))
    list_simVa.append(round(Va_sim, 3))
    list_error.append(round(error, 3))
    list_Wdr.append(round(Wdr, 3))
    list_Vgs.append(round(Vgs, 3))
    list_Vth.append(round(Vth, 3))     
    
    print("\n\n\n-------------------------------------------------------------------")
    print("\n\n\n  Iteration    = ",itera)        
    print("  Initial Error=  {:.2E}  [%]".format(error))
    print("  Initial Ldr  =  {:.2E}  [\N{MICRO SIGN}m]".format(Ldr))
    print("  Initial Vth  =  {:.2E}  [V]".format(Vth))
    print("  Initial Vgs  =  {:.2E}  [V]".format(Vgs))
    print("  Initial Va   =  {:.2E}  [V]".format(Va_sim))
    
    itera += 1
    while(itera<15) :
        print("\n\n-------------------------------------------------------------------")
        print("\n\n  Iteration    = ",itera)
        Ldr, factor = guess_Ldr(Va_sim, Va_tar, error, Ldr)
        print("  Ldr          =  {:.2E}  [\N{MICRO SIGN}m]".format(Ldr))
        Vth = get_Vth (MOS, model_deck, Wdr, Ldr, Vsb)
        Vgs = Vov + Vth                                           # find vgs by vth
        Va_sim = calc_Va_sim(MOS, model_deck, Vds, Vgs, Wdr, Ldr)
        print("  Target Va    =  {:.2E}  [V]".format(Va_tar))
        print("  Simulated Va =  {:.2E}  [V]".format(Va_sim))
        error = calc_error(Va_sim, Va_tar)
        print("  Error        =  {:.3E} [%]".format(error))
        
        
        list_iteration.append(itera)
        list_factor.append(factor)
        list_Ldr.append(round(Ldr, 3))
        list_simVa.append(round(Va_sim, 3))
        list_error.append(round(error, 3))
        
        list_Wdr.append(round(Wdr, 3))
        list_Vgs.append(round(Vgs, 3))
        list_Vth.append(round(Vth, 3))
        
        
        if error < 0.1 : 
            Wdr, LINT, WINT, XL, XW = calc_Wdr(W_L, Ldr, model_deck, model_name)
            break;
        itera = itera + 1
        
    print("\n\n\n-------------------------------------------------------------------")     
    print("  iteration    = ",str(list_iteration))
    print("  factor       = ",str(list_factor))
    print("  Ldr          = ",str(list_Ldr) + " \N{MICRO SIGN}m")
    print("  Target Va    =  [{:.2E}] V".format(Va_tar))
    print("  SimVa        =  " + str(list_simVa) + " V")
    print("  Error        =  " + str(list_error) + " %")
    print("-------------------------------------------------------------------")
    
    print("\n\n\n\n-------------------------------------------------------------------")
    print("APPLICATION SPESIFIC VALUES:")
    print("    PDK    = ", model_deck)  
    print("    Model  = ", model_name)
    print("    LINT   = ", LINT)     
    print("    WINT   = ", WINT)     
    print("    XL     = ", XL)     
    print("    XW     = ", XW) 
    
    ngfunc.plot_lists(list_iteration, list_factor, list_Ldr, Va_tar, list_simVa, list_error)

    return LINT, WINT, XL, XW, Wdr, Ldr, Vgs


"""There are three different cases in the flowchart to be followed.
amplifier_driver_flowchart
current_source_sink_flowchart
unknown_flowchart #!!!!!

10/04/2021
"""   
def amplifier_driver_flowchart(MOS, model_deck, Vdsat, gm, gmb, rds) :
    Vov_Vdsat, Vov_gmId, Vov_gmbId, Vov_Ish, Vov_gmgmbId = ngbase.sort_graphs(MOS, model_deck)  
    Vov = get_pair(Vdsat, Vov_Vdsat, 0)
    gm_gmb_Id, Id = get_Id_by_gm_gmb(Vov, gm, gmb, Vov_gmId, Vov_gmbId) 
    Ish = get_pair(Vov, Vov_Ish, 1)                  #find I# by Vov
    W_L = Id/Ish                                  # -  W/L = I#/Id      
    Va_tar = Id*rds                               # - Va = (Id)x(rds)
    print("\nAMPLIFIER DRIVER PROBLEM:")
    print("  Vov          =  {:.2E} [V]".format(Vov))             # scientific notation and 2 decimal digits
    print("  gm(b)Id      =  {:.2E} [1/\u03A9]".format(gm_gmb_Id))
    print("  Id           =  {:.2E} [A]".format(Id)) 
    print("  I#           =  {:.2E} [A/sq]".format(Ish)) 
    print("  W/L          =  {:.2E} ".format(W_L)) 
    print("  Target Va    =  {:.2E} [V]" .format(Va_tar)) 
    return Vov, W_L, Va_tar
def current_source_sink_flowchart(MOS, model_deck, Id, gm, gmb, rds) :
    Vov_Vdsat, Vov_gmId, Vov_gmbId, Vov_Ish, Vov_gmgmbId = ngbase.sort_graphs(MOS, model_deck)
    Vov = get_Vov_by_gm_gmb_Id(Id, gm, gmb, Vov_gmId, Vov_gmbId)
    Ish = get_pair(Vov, Vov_Ish, 1)                  #find I# by Vov
    W_L = Id/Ish                                                  # -  W/L = I#/Id
    Va_tar = Id*rds                                               # - Va = (Id)x(rds)
    

    print("\nAMPLIFIER DRIVER PROBLEM:")
    print("  Vov          =  {:.2E} [V]".format(Vov))             # scientific notation and 2 decimal digits
    print("  Id           =  {:.2E} [A]".format(Id)) 
    print("  I#           =  {:.2E} [A/sq]".format(Ish)) 
    print("  W/L          =  {:.2E}".format(W_L)) 
    print("  Target Va    =  {:.2E} [V]" .format(Va_tar)) 
    return Vov, W_L, Va_tar
def unknown_flowchart(MOS, model_deck, Vdsat, Id, rds) :
    Vov_Vdsat, Vov_gmId, Vov_gmbId, Vov_Ish, Vov_gmgmbId = ngbase.sort_graphs(MOS, model_deck)  
    Vov = get_pair(Vdsat, Vov_Vdsat, 0)
    Ish = get_pair(Vov, Vov_Ish, 1)                  #find I# by Vov
    W_L = Id/Ish                                                  # -  W/L = I#/Id
    Va_tar = Id*rds                                               # - Va = (Id)x(rds)
    print("\nUNKOWN PROBLEM:")
    print("  Vov          =  {:.2E} [V]".format(Vov))             # scientific notation and 2 decimal digits
    print("  Id           =  {:.2E} [A]".format(Id)) 
    print("  I#           =  {:.2E} [A/sq]".format(Ish)) 
    print("  W/L          =  {:.2E}".format(W_L)) 
    print("  Target Va    =  {:.2E} [V]" .format(Va_tar)) 
    return Vov, W_L, Va_tar 



def guess_Ldr(Va_sim, Va_tar, error, Ldr) :
    factor = ngfunc.find_factor(error)
    print("  Factor       = ",factor) 
    if Va_sim < Va_tar :
        Ldr = abs(Ldr+(Ldr*factor))
    else :
        if Va_sim > Va_tar :
            Ldr = abs(Ldr-(Ldr*factor))
    return Ldr, factor
def calc_Va_sim (MOS, model_deck, Vds, Vgs, Wdr, Ldr) :
    if (MOS==1) :
        ngbase.n_Va_sp(model_deck, Vds, Vgs, Wdr, Ldr)  # simulate Va 
        Va_data = ngbase.n_sort_Va()
    else :
        ngbase.p_Va_sp(model_deck, Vds, Vgs, Wdr, Ldr)  # simulate Va 
        Va_data = ngbase.p_sort_Va() 
    Va_sim = Va_data[1][0,0]
    return Va_sim      
def calc_error(Va_sim, Va_tar) :
    error = abs(((Va_sim-Va_tar)/Va_tar))*100
    return error
def calc_Wdr (W_L, Ldr, model_deck, model_name) :
    LINT = float(ngfunc.extract_umc_param(model_deck, model_name, "LINT"))
    WINT = float(ngfunc.extract_umc_param(model_deck, model_name, "WINT"))
    XW = float(ngfunc.extract_umc_param(model_deck, model_name, "XW"))
    XL = float(ngfunc.extract_umc_param(model_deck, model_name, "XL"))        
    L = Ldr + XL - (2*LINT)
    W = (W_L)*L
    Wdr = W - XW + (2*WINT)
    
 
    return Wdr, LINT, WINT, XL, XW 

"""  Calculation of the iteration factor. 
Considering the error percentage, determine a multiplication factor
to find Ldr with less iteration count.
This method can be further improved.
09/03/2021
"""    
def find_factor(error):
    
    error = error/100
    # if  0 <= error < 0.005 :
    #     factor = 0.001
    # else :
    #     if 0.005 <= error < 0.01 :
    #         factor = 0.005                        
    #     else :
    if 0 <= error < 0.025 :
        factor = 0.01
    else :
        if 0.025 <= error < 0.05 :
            factor = 0.05
        else :
            if 0.05 <= error < 0.1 :
                factor = 0.1
            else :  
                if 0.1 <= error < 0.5 :
                    factor = 0.3
                else :
                    if 0.5 <= error < 1 :
                        factor = 0.5
                    else :
                        factor = 0.6 
    return factor


""" Extract a value from its pair element index.

get_Vov_by_Vdsat
get_gmbId_by_Vov
get_Id_by_gm_gmb
get_Ish_by_Vov
get_Vov_by_gm_gmb_Id
"""
def get_pair(value, ext_data, col):
    idx = ngfunc.find_nearest(ext_data[not col], value)     # find index of nearest element in the data
    result = ngbase.get_col_elem(ext_data, idx, col)   # use index and find the pair in an extracted data pair
    return result

def get_Id_by_gm_gmb(Vov, gm, gmb, Vov_gmId, Vov_gmbId):
    if (gm) :      
        gmId = get_pair(Vov, Vov_gmId, 1)       #find gm/Id by Vov   
        Id = gm / gmId
        return gmId, Id
    elif (gmb) :
        gmbId = get_pair(Vov, Vov_gmbId, 1)    #find gm/Id by Vov   
        Id = gmb / gmbId
        return gmbId, Id

def get_Vov_by_gm_gmb_Id(Id, gm, gmb, Vov_gmId, Vov_gmbId):
    if(gm) :
        gm_Id = gm / Id
        Vov = get_pair(gm_Id, Vov_gmId, 0)
    elif(gmb) :
        gmb_Id = gmb / Id
        Vov = get_pair(gmb_Id, Vov_gmbId, 0)
    return Vov

def get_Vth (MOS, model_deck, Wdr, Ldr, Vsb):
    Vsb_Vth = ngbase.sort_Vsb_Vth (MOS, model_deck, Wdr, Ldr)
    Vth = get_pair(Vsb, Vsb_Vth, 1)
    return Vth






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