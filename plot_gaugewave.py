"""
plot_gaugewave.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 15:10:32 (jonah)>

This is a library containing a few simple tools for plotting a
gaugewave. It contains constants like the amplitude.

We often mention the value Txx. Txx is the xx-component of whatever
tensor we want to plot. In the case of the gaugewave, the xx-component
is the component we care about.
"""


# Imports
# ----------------------------------------------------------------------
import numpy as np # For array support
from scipy.optimize import curve_fit
import extract_tensor_data as etd # For tensor support
# Plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------


# Global Constants
# ----------------------------------------------------------------------
D = 1 # The period of the wave.
A = 0.5 # The amplitude of the wave.
COORD = 0 # The x coordinate
E_INDEX=(0,0) # The xx component of the extrinsic curvature tensor
RESOLUTION = 200 # Resolution for plot_kxx or plot_gxx
my_linewidth = 5
fontsize = 20
xlabel = "Position"
# True if the errors are divided by h^4. False otherwise.
SCALE_ERRORS = True
ACCEPTABLE_ERROR = 1E-14
EXPONENT = -4
ERR_LABEL_MODIFIER = r'$/h^4$'
# Mark true for debugging statements
DEBUGGING = False
# ----------------------------------------------------------------------


def get_Txx_data(time,filename_list):
    """
    Takes a list of filenames (strings) and generates three lists,
    positions_list, Txx_list, time_index_list. positions_list contains
    positions data as described in extract_tensor_data.py. Txx_list
    contains data the xx-element of the symmetric tensor we wish to
    investigate for each file.

    time_index_list defines the time iteration at which the data is
    extracted.

    Also returns lattice spacing, which is the spacing between
    points. We call the lattice spacing h. Returns a list, h for every
    file.
    """
    positions_list = []
    Txx_list = []
    time_index_list = []
    h_list = []
    for filename in filename_list:
        data = etd.extract_data(filename)
        times = [snapshot[0][4] for snapshot in data]
        # time_index = etd.find_largest_index_of_subvalue(times,time)
        time_index = times.index(time) # Raises error if times are not exact
        position,Txx=etd.element_of_position_at_time(E_INDEX[0], E_INDEX[1],
                                                     COORD, time_index, data)
        time_index_list.append(time_index)
        positions_list.append(position)
        Txx_list.append(Txx)
        h_list.append(etd.get_lattice_spacing(data))
    return positions_list,Txx_list,time_index_list,h_list


def get_xy_pair(function,xmin,xmax,time):
    """
    returns two arrays, x and y. x is a linspace xmin to xmax and
    y is function(x,time)
    """
    x = np.linspace(xmin,xmax,RESOLUTION)
    y = function(x,time)
    return x,y


def get_difference(positions,Txxs):
    """
    Assumed that positions is a list of [position1,position2] and
    Txxs is a list of [Txx1,Txx2]
    Returns a list of positions and tensors that is the difference
    between Txx1 and Txx2 at the courser positions
    """
    course_index = 0 if len(positions[0]) < len(positions[1]) else 1
    other_index = 0 if course_index == 1 else 1
    pos = []
    difference = []
    same_position = lambda i,j: positions[course_index][i] \
        - positions[other_index][j] < ACCEPTABLE_ERROR
    for i in range(len(positions[course_index])):
        for j in range(len(positions[other_index])):
            if same_position(i,j) and positions[course_index][i] not in pos:
                pos.append(positions[course_index][i])
                difference.append(Txxs[course_index][i] \
                                      - Txxs[other_index][j])
    return pos,difference

def plot_Txx(positions_list,Txx_list,name_list,time,ylabel,function):
    """
    Plots the theoretical value for Txx, the xx-component of the
    tensor we're interested in at the time (not time index) and
    compares it to the same plots stored in positions_list and
    Txx_list. Uses the name_list for a legend.

    ylabel is the label for the y-axis function is the theoretical
    function for the xx-component of the tensor.
    """
    # Find plot domain
    xmin = min([min(position) for position in positions_list])
    xmax = max([max(position) for position in positions_list])
    
    # Get theoretical data
    theoretical_positions,theoretical_Txx = get_xy_pair(function,
                                                        xmin,xmax,time)
    
    # Change font size
    mpl.rcParams.update({'font.size': fontsize})
    # Define plots
    lines = [plt.plot(theoretical_positions,theoretical_Txx,
                      linewidth=my_linewidth)]
    lines += [plt.plot(positions_list[i],Txx_list[i],linewidth=my_linewidth) \
                  for i in range(len(positions_list))]
    # Plot parameters
    plt.xlim([xmin,xmax])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Gaugewave {} after {} crossing times".format(ylabel,time))
    plt.legend(["theoretical value"] + name_list)
    plt.show()
    return


def get_error(function,position,Txx,time):
    """
    Takes the position and Txx data for a given spacetime and
    calculates the error data at a given time.
    """
    return function(position,time) - Txx


def find_Txx_phase_shift(function,position,Txx):
    """
    Uses curve fitting to solve the time to evaluate
    position(position,time) if time is a free parameter. Equivalent to
    solving for the phase shift at time zero.
    """
    popt,pcov = curve_fit(function,position,Txx)
    phi = popt[0]
    return phi

def plot_errors(function,positions_list,Txx_list,
                h_list,name_list,time,ylabel,err_label,
                divide_by_h_to_the_4,
                fix_offset,
                fix_phase):
    """
    Plots the error for every datafile in the filename list. May scale
    by dividing by h^4 if this is set. Requires the positions_list and
    Txx_list already extracted.

    h is the lattice spacing.
    """
    # Exponent to scale errors by
    exponent = EXPONENT if divide_by_h_to_the_4 else 0.0

    # Center the kxx lists around their average
    if fix_offset:
        crude_average = lambda x: 0.5*(np.max(x) + np.min(x))
        Txx_list = [Txx - crude_average(Txx) for Txx in Txx_list]
        if DEBUGGING:
            print "Fixing offset."
    if fix_phase:
        phi_list = [find_Txx_phase_shift(function,positions_list[i],Txx_list[i])\
                        for i in range(len(Txx_list))]
        errors = [get_error(function,positions_list[i],
                            Txx_list[i],phi_list[i]) for i in range(len(Txx_list))]
        if DEBUGGING:
            print "Fixing phase."
                            
    else:
        errors = [get_error(function,positions_list[i],Txx_list[i],time)\
                      for i in range(len(Txx_list))]
        phi_list = [time for i in range(len(Txx_list))]
    if DEBUGGING:
        for i in range(len(Txx_list)):
            x,y = get_xy_pair(function,np.min(positions_list[i]),
                              np.max(positions_list[i]),
                              phi_list[i])
            plt.plot(positions_list[i],Txx_list[i],x,y)
            plt.show()
            print "{} has max error {}".format(name_list[i],
                                                np.max(errors[i]))
            print "\t has {} grid points".format(len(errors[i]))
            print "\t has lattice spacing {}".format(h_list[i])

    # Define errors to the fourth power
    h4_errors = [(h_list[i]**(exponent))*errors[i] \
                     for i in range(len(Txx_list))]

    # Change font size
    mpl.rcParams.update({'font.size': fontsize})
    # Define plots
    lines = [plt.plot(positions_list[i],h4_errors[i],linewidth=my_linewidth)\
                 for i in range(len(positions_list))]
    # Plot parameters
    plt.title("Gaugewave {} after {} crossing times".format(err_label,time))
    plt.xlabel(xlabel)
    plt.ylabel(err_label)
    plt.legend(name_list)
    plt.show()
    return


if __name__=="__main__":
    raise ImportWarning(etd.WARNING_MESSAGE)
