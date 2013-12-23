#!/usr/bin/env python2

"""
plot_gaugewave.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2013-12-23 15:45:16 (jonah)>

This program plots the gauge wave at time index i of every input file
and compares it to the expected gaugewave.
Example call:
python2 plot_gaugewave.py 0 *curv.x.asc
"""

# Imports
# ----------------------------------------------------------------------
import extract_tensor_data as etd
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
D = 1 # The period of the wave.
A = 0.1 # The amplitude of the wave.
COORD = 0 # The x coordinate
E_INDEX=(0,0) # The xx component of the extrinsic curvature tensor
KXX_RESOLUTION = 200 # Resolution for plot_kxx
# ----------------------------------------------------------------------


def gaugewave_kxx(x,t):
    """
    The analytic form of the kxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    numerator = -np.pi*A*np.cos(2*np.pi*(x-t)/d)
    denominator = d*np.sqrt(1-A*np.sin(2*np.pi*(x-t)/d))
    return numerator/denominator


def get_kxx_data(t_index,filename_list):
    """
    Takes a list of filenames (strings) and generates three lists,
    positions_list, kxx_list, time_list. positions_list contains positions
    data as described in extract_tensor_data.py. kxx_list contains
    data the xx-element of the curvature tensor for each file.

    t_index defines the time iteration at which the data is extracted.

    time_list lists the times that the functions are evaluated at at a
    given iteration.
    """
    positions_list = []
    kxx_list = []
    time_list
    for filename in filename_list:
        data = etd.extract_data(filename)
        position,kxx=etd.element_of_position_at_time(E_INDEX[0], E_INDEX[1],
                                                     COORD, t_index, data)
        time_list.append(data[t_index][4])
        positions_list.append(position)
        kxx_list.append(kxx)
    return positions_list,kxx_list,time_list


def get_theoretical_kxx(xmin,xmax,time):
    """
    Generates the theoretical value for kxx from xmin to xmax over time.
    """
    x = np.arange(xmin,xmax,KXX_RESOLUTION)
    y = gaugewave(x,time)
    return x,y

def plot_kxx(positions_list,kxx_list,filename_list,time):
    """
    Plots the theoretical value for kxx at the time (not time index)
    and compares it to the same plots stored in positions_list and
    kxx_list. Uses the filename_list for a legend.
    """
    
