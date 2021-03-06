#!/usr/bin/env python2

"""
plot_robust_stability_at_time_multipatch.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 11:14:58 (jonah)>

This is a program that plots the (x,y)-component of the 3-metric at a
given time of a spacetime generated by the robust stability test. This
spacetime should be Minkowski space, where g_{xy} should be zero. So
we can think of this term as the error.

We project along the x-axis.

Adapted for multipatch. Plots based on directory, not based on
position

Example call:
python2 plot_robust_stability_at_time.py time directory1 directory2 directory3

where time is the time you want to plot at. Make sure that a snapshot
exists at this time for all spacetimes you want to plot. Otherwise the

program will raise an error.
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # For array support
import os # For operating system support
import sys # For globbing support
# plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# Other important pieces of the toolbox
import extract_tensor_data_multipatch as multipatch
import simfactory_interface as interface
import plot_gaugewave_multipatch as pgm
import plot_robust_stability_at_time as prst
# ----------------------------------------------------------------------

def get_Txy_data(time,directory_list,file_name=False):
    """
    Takes a list of directorys (strings) and generates three lists,
    positions_list, Txy_list, time_index_list. positions_list contains
    positions data as described in extract_tensor_data.py. Txy_list
    contains data the xy-element of the symmetric tensor we wish to
    investigate for each file.

    time_index_list defines the time iteration at which the data is
    extracted.

    Also returns lattice spacing, which is the spacing between
    points. We call the lattice spacing h. Returns a list, h for every
    file.

    file_name gives the name of the file containing the tensor
    data. Defaults to the metric data projected along the x-axis.

    This method is adapted for multipatch.
    """
    time = float('%.10f' % time)
    positions_list = []
    Txy_list = []
    time_index_list = []
    h_list = []
    num_cells_list = []
    for directory in directory_list:
        tensor_data,coordinate_maps,h,num_cells = pgm.generate_map_resolution_and_tensor_data(directory,pgm.RESTART_NUMBER,file_name)
        times = [float('%.10f' % snapshot[0][4]) for snapshot in tensor_data]
        time_index = times.index(time) # Raises an error if the appropriate time doesn't exist
        position,Txy = multipatch.element_of_position_at_time(prst.T_INDEX[0],prst.T_INDEX[1],prst.COORD,time_index,tensor_data,coordinate_maps)
        time_index_list.append(time_index)
        positions_list.append(position)
        Txy_list.append(Txy)
        h_list.append(h)
        num_cells_list.append(num_cells)
    return positions_list,Txy_list,time_index_list,h_list,num_cells_list

def plot_Txy(positions_list,Txy_list,num_cells_list,time):
    """
    Plots the theoretical value for Txy, the xy-component of the
    tensor we're interested in at the time (not time index) and
    compares it to the same plots stored in positions_list and
    Txy_list.
    """
    name_list = ["{} Cells".format(i) for i in num_cells_list]
    prst.plot_Txy(positions_list,Txy_list,name_list,time)
    return

def main(time,directory_list):
    """
    Plots gxy for every file in the file list at a given time
    """
    positions_list,gxy_list,time_list,h_list,num_cells_list = get_Txy_data(time,directory_list)
    plot_Txy(positions_list,gxy_list,num_cells_list,time)
    return

if __name__ == "__main__":
    time= float(sys.argv[1])
    file_list = sys.argv[2:]
    main(time,file_list)
