#!/usr/bin/env python2

"""
plot_gaugewave_kxx.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-02 20:04:13 (jonah)>

This program plots the extrinsic curvature gauge wave at time index t
of every input file and compares it to the expected gaugewave.

Generates two plots. The first plot is just the analytic gaugewave and
the solution gaugewave. The second is the error.

Example call:
python2 plot_gaugewave_kxx.py 0 *curv.x.asc
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
ylabel = r'$K_{xx}$'
# Error plot y axis label
err_label = ylabel + " error"
if pg.SCALE_ERRORS:
    err_label += pg.ERR_LABEL_MODIFIER
# Mark true if you want to examine error without phase or offset shift
FIX_PHASE = True
FIX_OFFSET = True
# ----------------------------------------------------------------------

def gaugewave_kxx(x,t):
    """
    The analytic form of the kxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    numerator = -np.pi*pg.A*np.cos(2*np.pi*(x-t)/pg.D)
    denominator = pg.D*np.sqrt(1-pg.A*np.sin(2*np.pi*(x-t)/pg.D))
    return numerator/denominator


def get_kxx_data(time,filename_list):
    """
    Takes a list of filenames (strings) and generates three lists,
    positions_list, kxx_list, time_index_list. positions_list contains
    positions data as described in extract_tensor_data.py. kxx_list
    contains data the xx-element of the curvature tensor for each
    file.

    time_index_list defines the time iteration at which the data is
    extracted.

    Also returns lattice spacing, which is the spacing between
    points. We call the lattice spacing h. Returns a list, h for every
    file.
    """
    return pg.get_Txx_data(time,filename_list)


def plot_kxx(positions_list,kxx_list,filename_list,time):
    """
    Plots the theoretical value for kxx at the time (not time index)
    and compares it to the same plots stored in positions_list and
    kxx_list. Uses the filename_list for a legend.
    """
    pg.plot_Txx(positions_list,kxx_list,filename_list,
                time,ylabel,gaugewave_kxx)

    
def plot_h4_errors(positions_list,kxx_list,h_list, filename_list,time):
    """
    Plots h^4 * error for every datafile in the filename
    list. Requires the positions_list and kxx_list already extracted.

    h is the lattice spacing.
    """
    pg.plot_errors(gaugewave_kxx,positions_list,kxx_list,h_list,
                   filename_list, time, ylabel,err_label,
                   pg.SCALE_ERRORS,FIX_PHASE,FIX_OFFSET)

    
def main(time,file_list):
    """
    Plots kxx for every file in file list at the given time.
    """
    positions_list,kxx_list,time_list,h_list = get_kxx_data(time,file_list)
    plot_kxx(positions_list,kxx_list,file_list,time)
    plot_h4_errors(positions_list,kxx_list,h_list,file_list,time)
    return


if __name__ == "__main__":
    time = float(sys.argv[1])
    file_list = sys.argv[2:]
    main(time,file_list)
