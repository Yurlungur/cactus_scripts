"""
plot_gaugewave.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-11 12:27:58 (jonah)>

This is a library containing a few simple tools for plotting a
gaugewave. It contains constants like the amplitude.

This version of the library is adapted for multipatch simulations.

We only plot the xx-component of the metric tensor in the multipatch
formulation.
"""

# Imports
# ----------------------------------------------------------------------

# Import standard tools
import numpy as np # For array support
from scipy.optimize import curve_fit
import os # For operating system support
# Plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# Import other pieces of the toolbox
import extract_tensor_data_multipatch as multipatch # For tensor
import simfactory_interface as interface # for simfactory support
# support We can still use the original plot gaugewave for a lot of
# stuff, so let's import that.
import plot_gaugewave as pg_original
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
D = pg_original.D # = 1. The period of the wave
A = pg_original.A # = 0.5. The amplitude of the wave.
COORD = pg_original.COORD # = 0. The x coordinate
E_INDEX = pg_original.E_INDEX # = (0,0) The xx component of extrinsic curvature
RESOLUTION = pg_original.RESOLUTION # = 200 Resolution for plot_kxx or plot_Txx
LINEWIDTH = pg_original.my_linewidth # = 5
FONTSIZE = pg_original.fontsize # = 20
XLABEL = pg_original.xlabel # "position"
YLABEL = r'$g_{xx}$'
ERR_LABEL_MODIFIER = pg_original.ERR_LABEL_MODIFIER # /h^4
ERR_LABEL = YLABEL + ERR_LABEL_MODIFIER
ACCEPTABLE_ERROR = pg_original.ACCEPTABLE_ERROR
EXPONENT = -4.0
RESTART_NUMBER = 0 # Restart number for the data directory
# For calculating the resolution
RESOLUTION_PARAMETER_STRING = "Coordinates::ncells_x"
DOMAIN_SIZE = 1
# Mark true for debugging statements
DEBUGGING = True
# Mark true if you want to examine error without phase or offset shift
FIX_PHASE = False
FIX_OFFSET = False
SCALE_ERRORS=True
# ----------------------------------------------------------------------

def generate_map_resolution_and_tensor_data(directory_name,
                                            restart_number=RESTART_NUMBER,
                                            file_name=False):
    """
    Takes a directory name and returns map data, tensor data, and
    resolution data.

    File name is the name of the file containing the tensor data. By
    default it is the metric tensor.
    """
    # File path stuff
    paths = interface.get_file_paths(directory_name,restart_number,file_name)
    directory_path = paths[0]
    tensor_path = paths[1]
    coordinates_path = paths[2]
    parameter_path = paths[3]
    # Extract the data
    tensor_data = multipatch.extract_data(tensor_path)
    coordinate_maps = multipatch.make_coordinate_maps(coordinates_path)
    number_of_cells = interface.extract_parameter_value(parameter_path,
                                                        RESOLUTION_PARAMETER_STRING,
                                                        True)
    # The resolution is the width of the coordinate space divided by
    # the number of cells
    resolution = float(DOMAIN_SIZE)/number_of_cells
    if DEBUGGING:
        print "num cells = {}".format(number_of_cells)
        print "h = {}".format(resolution)
    return tensor_data,coordinate_maps,resolution

def get_Txx_data(time,directory_list,file_name=False):
    """
    Takes a list of directories (strings) and generates three lists,
    positions_list, Txx_list, and time_index_list. positions_list
    contains positions data as described in
    extract_tensor_data.py. Txx_list contains position data for the
    xx-component of the metric tensor.

    time_index_list defines the time iteration at which the data is
    extracted.

    Also returns lattice spacing, which is the spacing between
    points. We call the lattice spacing h. Returns a single value of h
    per directory.

    file_name gives the name of the file containing the tensor
    data. Defaults to the metric data projected along the x-axis.

    This method is adapted for multipatch.
    """
    time = float('%.10f' % time)
    positions_list = []
    Txx_list = []
    time_index_list = []
    h_list = []
    for directory in directory_list:
        tensor_data,coordinate_maps,h = generate_map_resolution_and_tensor_data(directory,
                                                                                RESTART_NUMBER,
                                                                                file_name)
        times = [float('%.10f' % snapshot[0][4]) for snapshot in tensor_data]
        time_index = times.index(time) # Raises an error if the appropriate time doesn't exist
        position,Txx=multipatch.element_of_position_at_time(E_INDEX[0],E_INDEX[1],COORD,
                                                            time_index,
                                                            tensor_data,
                                                            coordinate_maps)
        time_index_list.append(time_index)
        positions_list.append(position)
        Txx_list.append(Txx)
        h_list.append(h)
    return positions_list,Txx_list,time_index_list,h_list

def plot_Txx(function,positions_list,Txx_list,directory_list,ylabel,time):
    """
    Plots the theoretical value for Txx at the time (not time index)
    and compares it to the same plots stored in positions_list and
    Txx_list. Uses the directory_list for a legend.

    Function is the theoretical function for the xx-component of the
    tensor. Given for the domain at hand
    """
    pg_original.plot_Txx(positions_list,Txx_list,directory_list,time,ylabel,function)
    return

def plot_errors(function,positions_list,Txx_list,
                h_list,directory_list,time,ylabel,err_label,
                fix_offset=False,fix_phase=False):
    """
    Plots the error for every datafile in the filename list. Rescales
    by 1/h^4. Requires the positions_list and Txx_list already
    extracted.

    h is the lattice spacing.

    fix_offset and fix_phase allow the user to align the data before
    comparing it to the analytic solution. In general, these features
    should be left off.
    """
    pg_original.plot_errors(function,positions_list,
                            Txx_list,h_list,directory_list,time,
                            ylabel,err_label,SCALE_ERRORS,
                            fix_offset,fix_phase)
    return

def generate_it_all(function,arguments,ylabel,file_name=False):
    """
    Essentially a main function. Wraps everything we care about in one
    neat little package. function must be given. Arguments emerges
    from sys.argv.
    
    file_name gives the name of the file containing the tensor
    data. Defaults to the metric data projected along the x-axis. It
    must be given. By default it points to the file for the metric
    tensor projected along the x-axis.

    ylabel is given
    """
    err_label = "({} error)".format(ylabel) + ERR_LABEL_MODIFIER
    time = float(arguments[1])
    directory_list = arguments[2:]
    positions_list,Txx_list,time_list,h_list = get_Txx_data(time,directory_list,file_name)
    plot_Txx(function,positions_list,Txx_list,directory_list,ylabel,time)
    plot_errors(function,positions_list,Txx_list,h_list,directory_list,
                time,ylabel,err_label,False,False)
    return

if __name__=="__main__":
    raise ImportWarning(multipatch.WARNING_MESSAGE)
