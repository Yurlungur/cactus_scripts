#!/usr/bin/env python2

"""
plot_gaugewave_of_time.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-02-07 18:01:28 (jonah)>

This is a simple library to plot the norm of g_{xx} as a function of
time for a gaugewave. Several gaugewave files can be plotted at the
same time.

Example call
python2 plot_gaugewave_of_time.py *.metric.x.asc
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # For array support
import extract_tensor_data as etd # For tensor support
import plot_gaugewave as pg
# Optimization tools
from scipy.optimize import curve_fit
# Plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# Linear algebra
from numpy.linalg import norm
# For command line
import sys
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
NORM_ERROR_TITLE = "{}-norm of Gaugewave {} Error as a Function of Time"
XLABEL = "Time (in wave periods)"
NORM_ERROR_Y_LABEL = "{}-norm({})"
T_INDEX = (0,0) # The indices of the element of the tensor we care about
LINEWIDTH = 5
FONTSIZE = 20
COORD = 0 # The x coordinate
ORDER = 2 # Order of norm
TENSOR_NAME = r'$g_{xx}$' # Name of the tensor we want to plot
RK_ORDER=4
# ----------------------------------------------------------------------


def gaugewave_gxx(x,t,A,D):
    """
    The analytic form of the gxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    return 1 - A*np.sin(2*np.pi*(x-t)/D)


def gaugewave_kxx(x,t,A,D):
    """
    The analytic form of the kxx component of a gaugewave as a
    function of x and t. It is independent of y and z.
    """
    numerator = -np.pi*A*np.cos(2*np.pi*(x-t)/D)
    denominator = D*np.sqrt(1-A*np.sin(2*np.pi*(x-t)/D))
    return numerator/denominator


def get_Tij_data_of_index(i,j,coord,filename_list):
    """
    Takes a list of filenames (strings) and generates a list of
    "evolutions." Each evolution is a list containing snapshots for a
    given file and contains a list of snapshots of the form

    [time,positions,Tijs]

    where (positions,Tijs) are sufficient data to plot the Tij element
    of the tensor as a function of position along the coord-axis. time
    is the time of the snapshot.

    The function also returns an "h_list" containing the lattice
    spacing of the grid in the file for each file. Ordering is the
    same as filename list.
    """
    evolutions_list = []
    h_list = []
    for filename in filename_list:
        evolutions = []
        data = etd.extract_data(filename)
        for snapshot in data:
            time = snapshot[0][4]
            positions,Tijs = etd.element_of_position_at_snapshot(i,j,coord,
                                                                 snapshot)
            evolutions.append([time,positions,Tijs])
        evolutions_list.append(evolutions)
        h_list.append(etd.get_lattice_spacing(data))
    return evolutions_list,h_list


def get_norm_error(function,position,Tij,time,order=2):
    """
    Takes the position and Tij data for a given spacetime at a given
    time and calculates the norm of the error at that time.
    """
    return norm(pg.get_error(function,position,Tij,time),ord=order)


def get_norm_error_of_time(function,evolution,order=2):
    """
    Takes an evolution and calculates its distance from function as a
    function of time.
    """
    times = []
    errors = []
    for snapshot in evolution:
        times.append(snapshot[0])
        errors.append(get_norm_error(function,
                                     snapshot[1],snapshot[2],snapshot[0],
                                     order))
    times = np.array(times)
    errors = np.array(errors)
    return times,errors


def calculate_analytic_form(function,snapshot):
    """
    Takes a snapshot extracted from get_Tij_data_of_index at a time
    where it is known to be analytically correct and fits function to
    it. Returns a fitted function which should be the analytic
    solution.

    The function is assumed to be of the form
    f(x,t,A,D)

    where t is the time, x is the position, A is the amplitude, and D
    is the period.
    """
    # Convenience variables
    time = snapshot[0]
    positions = snapshot[1]
    Tijs = snapshot[2]
    assert len(positions) == len(Tijs)
    # Set the time in the function we want to fit
    func1 = lambda x,A,D: function(x,time,A,D)
    popt,pcov = curve_fit(func1,positions,Tijs)
    return lambda x,t: function(x,t,*popt)


def plot_norm_error_of_time(function_list,evolutions,filename_list,
                            h_list=False,
                            tensor_name=TENSOR_NAME,
                            order=ORDER,
                            rk_order=RK_ORDER):
    """
    Plots the norm of the error of the tensor extracted using
    get_Tij_data_of_index.

    function_list is a list of functions for the analytic
    solution---one for each filename.
    """
    norm_error_title = NORM_ERROR_TITLE
    xlabel = XLABEL
    norm_error_y_label = NORM_ERROR_Y_LABEL

    # First find the norm error as a function
    times_list = [None]*len(filename_list)
    errors_list = [None]*len(filename_list)
    for i in range(len(filename_list)):
        times,errors = get_norm_error_of_time(function_list[i],
                                              evolutions[i],order)
        times_list[i] = times
        errors_list[i] = errors

    # Change the font size
    mpl.rcParams.update({'font.size': FONTSIZE})

    # If an error list is included, rescale by the error
    if h_list:
        norm_error_title += '\nRescaled by Lattice Spacing'
        norm_error_y_label = 'Rescaled '+norm_error_y_label
        lines = [plt.loglog(times_list[i],(h_list[i]**(-rk_order))*errors_list[i],linewidth=LINEWIDTH) for i in range(len(times_list))]
    else:
        lines = [plt.loglog(times_list[i],errors_list[i],linewidth=LINEWIDTH)\
                     for i in range(len(times_list))]

    plt.legend(filename_list)
    # Plot parameters
    plt.title(norm_error_title.format(order,tensor_name))
    plt.xlabel(xlabel)
    plt.ylabel(norm_error_y_label.format(order,tensor_name))
    # Show plot
    plt.show()
    return


def main(filename_list):
    analytic_function = gaugewave_gxx # analytic function we use
    evolutions_list,h_list = get_Tij_data_of_index(T_INDEX[0],T_INDEX[1],
                                                   COORD,
                                                   filename_list)
    analytic_func_list = [calculate_analytic_form(analytic_function,evolutions_list[i][0]) for i in range(len(filename_list))]
    plot_norm_error_of_time(analytic_func_list,evolutions_list,filename_list,
                            False,TENSOR_NAME,ORDER,RK_ORDER)
    return


if __name__ == "__main__":
    main(sys.argv[1:])    
