#!/usr/bin/env python2

"""
plot_robust_stability_evolution.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 11:39:30 (jonah)>

This little program plots the L2 norm of the (x,y)-component of the
3-metric of the Minkowski spacetime as a function of time. This is
very useful for the robust stability Apples-With-Apples test.

Example call:
python2 plot_robust_stability_evolution.py directory1 directory2 directory3
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # Array support
import sys # command line IO
# plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
import simfactory_interface as interface
import plot_gaugewave_multipatch as pgm
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
TIME_INDEX = 1 # index in numpy array for time
GXY_INDEX = 3 # index in numpy array for the (x,y)-component of the metric
LINEWIDTH=3
FONTSIZE=20
XLABEL = "Time"
YLABEL = r'$|g_{xy}|_2$'
TITLE = "Robust Stability Test Over Time"
RESOLUTION_PARAMETER_STRING = pgm.RESOLUTION_PARAMETER_STRING
DOMAIN_SIZE = pgm.DOMAIN_SIZE
RELEVANT_FILE_NAME = interface.ADM_PREFACTOR\
    +'metric.norm2'\
    +interface.ASCII_POSTFACTOR
# Whether to plot the y-axis as a log
PLOT_LOG=False
# ----------------------------------------------------------------------

def get_resolution_and_tensor_data(directory_name,
                                   restart_number=interface.RESTART_NUMBER):
    """
    Takes a directory name and returns two lists. A list of data
    sets and a list of numbers of grid points.
    """
    paths = interface.get_file_paths(directory_name,restart_number,
                                     RELEVANT_FILE_NAME)
    directory_path = paths[0]
    tensor_path = paths[1]
    coordinates_path = paths[2]
    parameter_path = paths[3]
    # Extract the data
    tensor_data = np.loadtxt(tensor_path).transpose()
    number_of_cells = interface.extract_parameter_value(parameter_path,
                                                        RESOLUTION_PARAMETER_STRING,
                                                        True)
    return tensor_data,number_of_cells

def main(directory_list,plot_log):
    """
    Generates the plot from filename_list.
    """
    plot_function = plt.semilogy if plot_log else plt.plot
    # Get the data
    data_sets = [None]*len(directory_list)
    name_list = [None]*len(directory_list)
    for i in range(len(directory_list)):
        temp_data,num_cells = get_resolution_and_tensor_data(directory_list[i])
        data_sets[i] = temp_data
        name_list[i] = "{} Cells".format(num_cells)
    # Set up the plot
    mpl.rcParams.update({'font.size':FONTSIZE})
    lines = [plt.plot(data[TIME_INDEX],data[GXY_INDEX],linewidth=LINEWIDTH) for data in data_sets]
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(TITLE)
    plt.legend(name_list)
    plt.show()
    return

if __name__ == "__main__":
    main(sys.argv[1:],PLOT_LOG)
