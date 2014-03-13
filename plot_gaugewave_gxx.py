#!/usr/bin/env python2

"""
plot_gaugewave_gxx.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-11 01:23:24 (jonah)>

This program plots the xx component of the metric for a gauge wave at
time t of every input file and compares it to the expected gaugewave.

We generate two plots. The first plot is the analytic gaugewave and
the solution gaugewave. The second is the error.

Example call:
python2 plot_gaugewave_gxx.py 0 *.curv.x.asc
"""

# Imports
# ----------------------------------------------------------------------
import extract_tensor_data as etd # To deal with tensor ascii files
import plot_gaugewave as pg # Library for plotting gaugewave tensors
import numpy as np # For array support
import sys # For globbing support
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
ylabel = r'$g_{xx}$'
# Error plot y axis label
err_label = ylabel + " error"
if pg.SCALE_ERRORS:
    err_label += pg.ERR_LABEL_MODIFIER
# Mark true if you want to scale errors
SCALE_ERRORS = True # pg.SCALE_ERRORS # default
# Mark true if you want to examine error without phase or offset shift
FIX_PHASE = True
FIX_OFFSET = False
# ----------------------------------------------------------------------

def gaugewave_gxx(x,t):
    """
    The analytic form of the gxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    return 1 - pg.A*np.sin(2*np.pi*(x-t)/pg.D)

def main(time,filename_list):
    """
    Plots gxx for every file in the file list at the given time. 
    """
    positions_list,gxx_list,time_list,h_list = pg.get_Txx_data(time,
                                                               filename_list)
    pg.plot_Txx(positions_list,gxx_list,filename_list,time,ylabel,
                gaugewave_gxx)
    pg.plot_errors(gaugewave_gxx,positions_list,gxx_list,h_list,filename_list,
                   time,ylabel,err_label,SCALE_ERRORS,FIX_OFFSET,FIX_PHASE)
    return

if __name__ == "__main__":
    time = float(sys.argv[1])
    file_list = sys.argv[2:]
    main(time,file_list)
