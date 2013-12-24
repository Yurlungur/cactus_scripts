#!/usr/bin/env python2

"""
plot_gaugewave.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2013-12-23 23:56:31 (jonah)>

This program plots the gauge wave at time index i of every input file
and compares it to the expected gaugewave.

Generates two plots. The first plot is just the analytic gaugewave and
the solution gaugewave.

Example call:
python2 plot_gaugewave.py 0 *curv.x.asc
"""

# Imports
# ----------------------------------------------------------------------
import extract_tensor_data as etd # To deal with tensor ascii files
import numpy as np # For array support
# Plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys # For globbing support
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
D = 1 # The period of the wave.
A = 0.1 # The amplitude of the wave.
COORD = 0 # The x coordinate
E_INDEX=(0,0) # The xx component of the extrinsic curvature tensor
KXX_RESOLUTION = 200 # Resolution for plot_kxx
my_linewidth = 5
fontsize = 20
xlabel = "Position"
ylabel = r'$K_{xx}$'
err_label = r'$K_{xx}$' + " error"
# ----------------------------------------------------------------------


def find_largest_index_of_subvalue(collection, value):
    """
    Finds the index of the largest element in the collection less than
    value.
    """
    subcollection = filter(lambda x: x <= value, collection)
    return collection.index(max(subcollection))


def gaugewave_kxx(x,t):
    """
    The analytic form of the kxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    numerator = -np.pi*A*np.cos(2*np.pi*(x-t)/D)
    denominator = D*np.sqrt(1-A*np.sin(2*np.pi*(x-t)/D))
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
    positions_list = []
    kxx_list = []
    time_index_list = []
    h_list = []
    for filename in filename_list:
        data = etd.extract_data(filename)
        times = [snapshot[0][4] for snapshot in data]
        time_index = find_largest_index_of_subvalue(times,time)
        position,kxx=etd.element_of_position_at_time(E_INDEX[0], E_INDEX[1],
                                                     COORD, time_index, data)
        time_index_list.append(time_index)
        positions_list.append(position)
        kxx_list.append(kxx)
        h_list.append(etd.get_lattice_spacing(data))
    return positions_list,kxx_list,time_index_list,h_list


def get_theoretical_kxx(xmin,xmax,time):
    """
    Generates the theoretical value for kxx from xmin to xmax over time.
    """
    x = np.linspace(xmin,xmax,KXX_RESOLUTION)
    y = gaugewave_kxx(x,time)
    return x,y


def plot_kxx(positions_list,kxx_list,filename_list,time):
    """
    Plots the theoretical value for kxx at the time (not time index)
    and compares it to the same plots stored in positions_list and
    kxx_list. Uses the filename_list for a legend.
    """
    # Find plot domain
    xmin = min([min(position) for position in positions_list])
    xmax = max([max(position) for position in positions_list])
    
    # Get theoretical data
    theoretical_positions,theoretical_kxx = get_theoretical_kxx(xmin,xmax,time)
    
    # Change font size
    mpl.rcParams.update({'font.size': fontsize})
    # Define plots
    lines = [plt.plot(theoretical_positions,theoretical_kxx,
                      linewidth=my_linewidth)]
    lines += [plt.plot(positions_list[i],kxx_list[i],linewidth=my_linewidth) \
                  for i in range(len(positions_list))]
    # Plot parameters
    plt.xlim([xmin,xmax])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Guagewave after {} crossing times".format(time))
    plt.legend(["theoretical value"] + filename_list)
    plt.show()
    return

def get_error(position,kxx,time):
    """
    Takes the position and kxx data for a given spacetime and
    calculates the error data at a given time.
    """
    return gaugewave_kxx(position,time) - kxx

def plot_h4_errors(positions_list,kxx_list,h_list, filename_list,time):
    """
    Plots h^4 * error for every datafile in the filename
    list. Requires the positions_list and kxx_list already extracted.

    h is the lattice spacing.
    """
    # Define errors to the fourth power
    h4_errors = [(h_list[i]**4)*get_error(positions_list[i],kxx_list[i],time)\
                     for i in range(len(kxx_list))]
    # Change font size
    mpl.rcParams.update({'font.size': fontsize})
    # Define plots
    lines = [plt.plot(positions_list[i],h4_errors[i],linewidth=my_linewidth)\
                 for i in range(len(positions_list))]
    # Plot parameters
    plt.title("Guagewave error after {} crossing times".format(time))
    plt.xlabel(xlabel)
    plt.ylabel(err_label)
    plt.legend(filename_list)
    plt.show()
    return
    

def main(time,file_list):
    """
    Plots kxx for every file in file list at the given time
    index. Time asumed to be fixed as the first time in time_list.
    """
    positions_list,kxx_list,time_list,h_list = get_kxx_data(time,file_list)
    plot_kxx(positions_list,kxx_list,file_list,time)
    plot_h4_errors(positions_list,kxx_list,h_list,file_list,time)
    return

if __name__ == "__main__":
    time = float(sys.argv[1])
    file_list = sys.argv[2:]
    main(time,file_list)
