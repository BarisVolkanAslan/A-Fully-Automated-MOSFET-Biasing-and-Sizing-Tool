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
import math
import time


#####################################################################



"""  Define global path locations of txt files and netlists."""
def define_global_paths():
    global raw_data_path
    raw_data_path = "sim_data/TSMC/"

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


    global n_verify_txt_path
    global n_verify_cir_path
    n_verify_txt_path = 'n_results.txt'
    n_verify_cir_path = 'n_results.cir'
    
    global p_verify_txt_path
    global p_verify_cir_path
    p_verify_txt_path = 'p_results.txt'
    p_verify_cir_path = 'p_results.cir'
    


#####################################################################

""" Create a .cir file from a given netlist and run it. 
"""
def run_circuit(model_deck, netlist, netlist_path, iter_speed) :
    with open(raw_data_path + netlist_path, 'w') as fh:
        fh.write(netlist)
    time.sleep(iter_speed)    
    os.startfile(os.path.normpath(raw_data_path + netlist_path))
    time.sleep(iter_speed)    
    
"""  Ngspice: NMOS device simulation
Create 'nmos1.cir' file to run. This document generates
5 different output documents formatted as '.txt'.
The output data included documents represent:
    1- Vdssat vs Vov,
    2- Id vs Vov,
    3- gm/Id vs Vov,
    4- gmb/Id vs Vov,
    5- (gm+gmb)/Id vs Vov,
    
    Vds = 0.9 if not given
    
respectively.
08/03/2021
"""
def n_mos1_sp(model_deck, Vds, Vsb, iter_speed) :    
    netlist = """ 
        .incl #
        m 2 1 3 0 cmosn w=6u l=0.8u
        vds 2 3 {:.2e}
        vgs 1 3
        vsb 3 0 {:.2e}
        .dc vgs 0.2 1.3 1m
        .save @m[vth] @m[vdsat] @m[id] @m[gm] @m[gmbs] v(1,3)
        .control
        set noaskquit
        run
        wrdata $ @m[vdsat] vs v(1,3)-@m[vth]
        wrdata % @m[id]/7.81 vs v(1,3)-@m[vth]
        wrdata ^ @m[gm]/@m[id] vs v(1,3)-@m[vth]
        wrdata & @m[gmbs]/@m[id] vs v(1,3)-@m[vth]
        wrdata ! (@m[gm]+@m[gmbs])/@m[id] vs v(1,3)-@m[vth]
        quit    
        .endc
        .end
        """.format(Vds, Vsb)

    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + n_Vdsat_Vov_txt_path)\
        .replace("%", raw_data_path + n_Ish_Vov_txt_path).replace("^", raw_data_path + n_gmId_Vov_txt_path)\
            .replace("&", raw_data_path + n_gmbId_Vov_txt_path).replace("!", raw_data_path + n_gmgmbId_Vov_txt_path)  
    run_circuit(model_deck, netlist_new, n_mos1_cir_path, iter_speed)
    
"""  Ngspice: PMOS device simulation

Create 'p_mos1.cir' file to run. This document generates
5 different output documents formatted as '.txt'.
The output data included documents represent:
    1- Vdssat vs Vov,
    2- Id vs Vov,
    3- gm/Id vs Vov,
    4- gmb/Id vs Vov,
    5- (gm+gmb)/Id vs Vov,
    
    Vds = -0.9 if not given
    
respectively.
08/03/2021
"""
def p_mos1_sp(model_deck, Vds, Vsb, iter_speed) :       
    netlist = """ 
        .incl #
        m 2 1 3 0 cmosp w=6u l=0.8u
        vds 2 3 {:.2e}
        vgs 1 3
        vsb 3 0 {:.2e}
        .dc vgs -1.3 -0.2 1m
        .save @m[vth] @m[vdsat] @m[id] @m[gm] @m[gmbs] v(1,3)
        .control
        set noaskquit
        run
        wrdata $ -@m[vdsat] vs v(1,3)+@m[vth]
        wrdata % @m[id]/8.08 vs v(1,3)+@m[vth]
        wrdata ^ @m[gm]/@m[id] vs v(1,3)+@m[vth]
        wrdata & @m[gmbs]/@m[id] vs v(1,3)+@m[vth]
        wrdata ! (@m[gm]+@m[gmbs])/@m[id] vs v(1,3)+@m[vth]
        quit    
        .endc
        .end
        """.format(Vds, Vsb)
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + p_Vdsat_Vov_txt_path)\
    .replace("%", raw_data_path + p_Ish_Vov_txt_path).replace("^", raw_data_path + p_gmId_Vov_txt_path)\
    .replace("&", raw_data_path + p_gmbId_Vov_txt_path).replace("!", raw_data_path + p_gmgmbId_Vov_txt_path) 
    run_circuit(model_deck, netlist_new, p_mos1_cir_path, iter_speed)
    
    
    
        
"""  Ngspice: Calculate Early Voltage (Va)
Calculate Early Voltage (Va) value of an NMOS device through the below 
netlist and generate a '.txt' formatted output file which contains 
the Va value.

This method is being used to reach the targetted Va value 
through an iterative process 

Targetted Va value has to be found before the iteration process
by some various methods.

Inputs for the method:
    1- vds
    2- vgs
    3- wdr
    4- ldr
08/03/2021
"""            
def n_Va_sp(model_deck, Vsb, Vds, Vgs, Wdr, Ldr, iter_speed) : 
    netlist = """ 
    .incl #
    m 2 1 3 0 cmosn w={:.2e}u l={:.2e}u
    vds 2 0 {:.2e}
    vgs 1 0 {:.2e}
    vsb 3 0 {:.2e}
    .op
    .control
    set noaskquit
    run
    wrdata $ @m[id]/@m[gds]
    quit
    .endc
    .end
    """.format(Wdr, Ldr, Vds, Vgs, Vsb)
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + n_Va_txt_path)           
    run_circuit(model_deck, netlist_new, n_Va_cir_path, iter_speed) 

"""  Ngspice: Calculate Early Voltage (Va)

Calculate Early Voltage (Va) value of an NMOS device through the below 
netlist and generate a '.txt' formatted output file which contains 
the Va value.

This method is being used to reach the targetted Va value 
through an iterative process 

Targetted Va value has to be found before the iteration process
by some various methods.

Inputs for the method:
    1- vds
    2- vgs
    3- wdr
    4- ldr
08/03/2021
"""            
def p_Va_sp(model_deck, Vsb, Vds, Vgs, Wdr, Ldr, iter_speed) : 
    netlist = """ 
    .incl #
    m 2 1 3 0 cmosp w={:.2e}u l={:.2e}u
    vds 2 3 {:.2e}
    vgs 1 3 {:.2e}
    vsb 3 0 {:.2e}
    .op
    .control
    set noaskquit
    run
    wrdata $ @m[id]/@m[gds]
    quit
    .endc
    .end
    """.format(Wdr, Ldr, Vds, Vgs, Vsb)
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + p_Va_txt_path)  
    run_circuit(model_deck, netlist_new, p_Va_cir_path, iter_speed)
    


    

    
    
"""  Ngspice: Calculate Threshold Voltage (Vth)

Vth depends on Ldr, which is the iteration variable.
Vth allows us to extract Vgs from Vov for a spesific channgel length l.
Inputs for the method:
    3- wdr
    4- ldr
08/03/2021
"""     
def n_Vth_sp(model_deck, Wdr, Ldr, Vds, Vsb, iter_speed) :
    netlist =""" 
        .incl #
        m 2 1 3 0 cmosn w={:.2e}u l={:.2e}u 
        vds 2 3 {:.2e}
        vgs 1 3 0.9
        vsb 3 0 {:.2e}
        .dc vsb 0 1.2 10m
        .control
        save @m[vth]
        set noaskquit
        run
        wrdata $ dc.@m[vth] 
        quit
        .endc
        .end
        """.format(Wdr, Ldr, Vds, Vsb) 
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + n_Vth_txt_path)
    run_circuit(model_deck, netlist_new, n_Vth_cir_path, iter_speed)
    
"""  Ngspice: Calculate Threshold Voltage (Vth)

Vth depends on Ldr, which is the iteration variable.
Vth allows us to extract Vgs from Vov for a spesific channgel length l.
Inputs for the method:
    3- wdr
    4- ldr
08/03/2021
"""     
def p_Vth_sp(model_deck, Wdr, Ldr, Vds, Vsb, iter_speed) :
    netlist =""" 
            .incl #
            m 2 1 3 0 cmosp w={:.2e}u l={:.2e}u 
            vds 2 3 {:.2e}
            vgs 1 3 -0.9
            vsb 3 0 {:.2e}
            .save @m[vth]
            .control
            dc vsb -1.2 0 10m
            set noaskquit
            run
            wrdata $ -@m[vth] 
            quit
            .endc
            .end
        """.format(Wdr, Ldr, Vds, Vsb) 
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + p_Vth_txt_path)  
    run_circuit(model_deck, netlist_new, p_Vth_cir_path, iter_speed)


def p_verify_sp(model_deck, Wdr, Ldr, Vgs, Vds, Vsb, iter_speed) :
    netlist ="""
        .incl #        
        m 2 1 3 0 cmosp w={:.2e}u l={:.2e}u
        vgs 1 3 {:.2e}
        vds 2 3 {:.2e}
        vsb 3 0 {:.2e}
        .op
        .control
        set noaskquit
        run
        wrdata $ @m[vdsat] @m[id]  @m[gm] @m[gmbs] 1/@m[gds]
        quit
        .endc
        .end""".format(Wdr, Ldr, Vgs, Vds, Vsb) 
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + p_verify_txt_path)  
    run_circuit(model_deck, netlist_new, p_verify_cir_path, iter_speed)

def n_verify_sp(model_deck, Wdr, Ldr, Vgs, Vds, Vsb, iter_speed) :
    netlist ="""
        .incl #        
        m 2 1 3 0 cmosn w={:.2e}u l={:.2e}u
        vgs 1 3 {:.2e}
        vds 2 3 {:.2e}
        vsb 3 0 {:.2e}
        .op
        .control
        set noaskquit
        run
        wrdata $ @m[vdsat] @m[id]  @m[gm] @m[gmbs] 1/@m[gds]
        quit
        .endc
        .end""".format(Wdr, Ldr, Vgs, Vds, Vsb) 
    netlist_new = netlist.replace('#', model_deck).replace("$", raw_data_path + n_verify_txt_path)  
    run_circuit(model_deck, netlist_new, n_verify_cir_path, iter_speed)

#####################################################################

""" Extract the pair value after sorting the graphical data.

out_data is the extracted graphical data
idx can be found with the function named find_nearest()
column can be 0 or 1; 0 is left hs., 1 is right hs..
"""
def get_col_elem(ext_data, idx, column):
    result = ext_data[column][0,idx]
    return result

def sort_graphs(MOS, model_deck, Vds, Vsb, iter_speed) :
    if (MOS) :
        if(Vds == 0):
            n_mos1_sp(model_deck, (0.9), Vsb, iter_speed)     # user choosed not to use Vds in flowchart section
        else :
            n_mos1_sp(model_deck, Vds, Vsb, iter_speed)           # generate fig3.8, fig3.12, fig3.10
        Vov_Vdsat   = sort_graphical_data(n_Vdsat_Vov_txt_path)     
        Vov_gmId    = sort_graphical_data(n_gmId_Vov_txt_path)       
        Vov_gmbId   = sort_graphical_data(n_gmbId_Vov_txt_path)     
        Vov_Ish     = sort_graphical_data(n_Ish_Vov_txt_path)         
        Vov_gmgmbId = sort_graphical_data(n_gmgmbId_Vov_txt_path)
    else :
        if(Vds == 0):
            p_mos1_sp(model_deck, (-0.9), Vsb, iter_speed)    # user choosed not to use Vds in flowchart section 
        else :
            p_mos1_sp(model_deck, Vds, Vsb, iter_speed)           # generate fig3.8, fig3.12, fig3.10
        Vov_Vdsat   = sort_graphical_data(p_Vdsat_Vov_txt_path)     
        Vov_gmId    = sort_graphical_data(p_gmId_Vov_txt_path)       
        Vov_gmbId   = sort_graphical_data(p_gmbId_Vov_txt_path)     
        Vov_Ish     = sort_graphical_data(p_Ish_Vov_txt_path)         
        Vov_gmgmbId = sort_graphical_data(p_gmgmbId_Vov_txt_path)
    return Vov_Vdsat, Vov_gmId, Vov_gmbId, Vov_Ish, Vov_gmgmbId

"""This method extracts output raw data of a chosen figure in book [1].
Simulation results which are .txt will be returned to a tuple of numpy arrays.

Early Voltage (Va) 
fig 3.7:  Threshold Voltage (Vth) 
fig 3.8:  Drain-Source Saturation Voltage (Vdssat) 
fig 3.8:  Sheet Current (Ish or I#) 
fig 3.12: Gate Transconductance Efficiency (gm/Id) 
fig 3.12: Bulk Transconductance Efficiency (gmb/Id) 
fig 3.12: Total Transconductance Efficiency ((gm+gmb)/Id) 

left column (0) vs right column (1):

Va              => (n_Va_txt_path)          or  (p_Va_txt_path)  
Vsb vs Vth      => (n_Vth_txt_path)         or  (p_Vth_txt_path)  
Vov vs Vdssat   => (n_Vdsat_Vov_txt_path)   or  (p_Vdsat_Vov_txt_path)
Vov vs I#       => (n_Ish_Vov_txt_path)     or  (p_Ish_Vov_txt_path) 
Vov vs gmId     => (n_gmId_Vov_txt_path)    or  (p_gmId_Vov_txt_path) 
Vov vs gmbId    => (n_gmbId_Vov_txt_path)   or  (p_gmbId_Vov_txt_path)
Vov vs gmgmbId  => (n_gmgmbId_Vov_txt_path) or  (p_gmgmbId_Vov_txt_path)

Created in 13 April 2021.
"""
def sort_graphical_data(txt_path) :
    out1_data_column2 = []
    out1_data_column1 = []
    os.getcwd()
    with open(raw_data_path + txt_path, 'r') as fh: 
        for line in fh:
            data_raw = np.asarray(line.rstrip().replace("e", "  ").split())
            data_raw = data_raw.astype(np.float)    
            data_raw[0] = round(data_raw[0] * math.pow(10,data_raw[1]), 10) #4th decimal point is being rounded
            data_raw[2] = round(data_raw[2] * math.pow(10,data_raw[3]), 10) #multiply with their power
            data_raw = np.delete(data_raw, 1) #remove unnecessary elements from the array
            data_raw = np.delete(data_raw, 2)             
            out1_data_column1.append(data_raw[0])
            out1_data_column2.append(data_raw[1])
    out1_data_column1 = np.asarray([out1_data_column1])      #left column
    out1_data_column1.astype(np.float)
    out1_data_column2 = np.asarray([out1_data_column2])      #right column
    out1_data_column2.astype(np.float)
    return (out1_data_column1, out1_data_column2)    


def sort_Vsb_Vth(sim_option, MOS, model_deck, Wdr, Ldr, Vds, Vsb, iter_speed):
    if (MOS) :
        if((sim_option == 0) or (sim_option == 1)) :
            n_Vth_sp(model_deck, Wdr, Ldr, Vds, Vsb, iter_speed)  # generate Vth graph with Ngspice
        else:
            n_Vth_sp(model_deck, Wdr, Ldr, (0.9), Vsb, iter_speed)
        Vsb_Vth = sort_graphical_data(n_Vth_txt_path)    # sort fig 3.8 Vsb vs Vth data   
    else :
        if((sim_option == 0) or (sim_option == 1)) :
            p_Vth_sp(model_deck, Wdr, Ldr, Vds, Vsb, iter_speed)
        else:
            p_Vth_sp(model_deck, Wdr, Ldr, (-0.9), Vsb, iter_speed)
        Vsb_Vth = sort_graphical_data(p_Vth_txt_path)
    return Vsb_Vth

def sort_Va(MOS, model_deck, Vsb, Vds, Vgs, Wdr, Ldr, iter_speed):
    if(MOS):
        n_Va_sp(model_deck, Vsb, Vds, Vgs, Wdr, Ldr, iter_speed)
        Va_data = sort_graphical_data(n_Va_txt_path)
    else:
        p_Va_sp(model_deck, Vsb, Vds, Vgs, Wdr, Ldr, iter_speed)
        Va_data = sort_graphical_data(p_Va_txt_path)
    return Va_data
    
def sort_results(txt_path, MOS, model_deck, Wdr, Ldr, Vgs, Vds, Vsb, iter_speed) :
    if (MOS):
        n_verify_sp(model_deck, Wdr, Ldr, Vgs, Vds, Vsb, iter_speed)
    else :
        p_verify_sp(model_deck, Wdr, Ldr, Vgs, Vds, Vsb, iter_speed)
    with open(raw_data_path + txt_path, 'r') as fh: 
        data_raw = fh.read().rstrip().split(" ")
        while("" in data_raw) :
            data_raw.remove("")
    results = []
    for ele in range(0,len(data_raw)):
        if ele % 2 == 1:
            results.append(data_raw[ele])
    vdsat = float(results[0])
    Id = float(results[1])
    gm = float(results[2])
    gmb = float(results[3])
    rds = float(results[4])
    
    if (MOS) :           
        try :
            os.remove(raw_data_path + "b3v32check.log")
        except :
            os.remove("b3v32check.log")
        os.remove(raw_data_path + n_verify_cir_path)
        os.remove(raw_data_path + n_verify_txt_path)
    else :
        try :
            os.remove(raw_data_path + "b3v32check.log")
        except :
            os.remove("b3v32check.log")
        os.remove(raw_data_path + p_verify_cir_path)
        os.remove(raw_data_path + p_verify_txt_path)
  
    return vdsat, Id, gm, gmb, rds
#####################################################################

define_global_paths()


#sub = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
#sup = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"

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