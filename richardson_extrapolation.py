#!/usr/bin/env python2

"""
richardson_extrapolation.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-18 00:48:47 (jonah)>

This program takes tensor ascii output from the einstein toolkit and
runs a Richardson extrapolation on the data to extract the convergence
order, the error factor due to the problem in question, and the true
solution.

The lattice spacing is calculated by studying the input files.

The program also plots a self-convergence test based on the data
given.

The syntax is:
python2 richardson_extrapolation.py time res1.asc res2.asc res3.asc

where time is the time in the evolution you want to compare at (the
time must exist for all three files), res1.asc is the lowest
resolution file, and res3 is the highest resolution file. (Any number
of files can be used, but the first file must be lowest resolution and
the last file must be the highest resolution. If this is not true, the
program will fix it for you.) All the resolutions must share some grid
points.
"""

# Imports
# ----------------------------------------------------------------------
import sys # FOr command line arguments
import numpy as np # For math and array support
import extract_tensor_data as etd
# Wrapper for the simplex function minimization algorithm
from scipy.optimize import fmin
# Plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
COORD = 0 # The coordinate along which the projection is based
E_INDEX=(0,0) # The component of the tensor we care about.
LINEWIDTH=5 # The plot linewidth
FONTSIZE=20 # The plot font size
PLOT_TITLE="Self Convergence Test at Time t = {}\norder = {}"
XLABEL="Position"
YLABEL="Rescaled Difference"
LEGEND_TEMPLATE="<h = {}> - <h = {}>"
ACCEPTABLE_ERROR=1E-14
XMIN=0
XMAX=1
# A marker we will place in the copied arrays
BAD_MARKER=None
FILTER_FUNCTION = lambda x: x != BAD_MARKER
# Just a convenient alias
ANDFUNC=lambda x,y: x and y
# Guess for the order of convergence
N0 = 4
# Filenames
FILE_PREFACTOR = "richardson."
ALPHA_FILE = FILE_PREFACTOR + "alpha.asc"
TRUE_SOLUTION_FILE = FILE_PREFACTOR + "true.asc"
# The interval for the bisection algorithm is [MIN_ORDER,MAX_ORDER]
MIN_ORDER = 0.5
MAX_ORDER = 6.5
# Condition for when a value is zero
EFFECTIVE_ZERO = 1E-10
# ----------------------------------------------------------------------


# Methods
# ----------------------------------------------------------------------
def get_tensor_data(time,filename_list):
    """
    Takes a list of filenames (strings) and generates three lists,
    positions_list, tensor_list, time_index_list. positions_list contains
    positions data as described in extract_tensor_data.py. tensor_list
    contains data the xx-element of the symmetric tensor we wish to
    investigate for each file.

    time_index_list defines the time iteration at which the data is
    extracted.

    Also returns lattice spacing, which is the spacing between
    points. We call the lattice spacing h. Returns a list, h for every
    file.
 
    Copied from plot_gaugewave.py
    """
    positions_list = []
    tensor_list = []
    time_index_list = []
    h_list = []
    for filename in filename_list:
        data = etd.extract_data(filename)
        times = [snapshot[0][4] for snapshot in data]
        # time_index = etd.find_largest_index_of_subvalue(times,time)
        time_index = times.index(time) # Raises error if times are not exact
        position,tensor=etd.element_of_position_at_time(E_INDEX[0], E_INDEX[1],
                                                     COORD, time_index, data)
        time_index_list.append(time_index)
        positions_list.append(position)
        tensor_list.append(tensor)
        h_list.append(etd.get_lattice_spacing(data))
    return positions_list,tensor_list,time_index_list,h_list


def sort_lists(positions_list,tensor_list,time_index_list,h_list,filename_list):
    """
    Takes a set of lists for data acquired by calling
    get_tensor_data(time,filename_list) and sorts the lists
    based on the resolutions.
    """
    resolution_map = {h_list[i] : (positions_list[i], tensor_list[i], time_index_list[i], filename_list[i]) for i in range(len(h_list))}
    h_list.sort()
    h_list.reverse()
    positions_list = [resolution_map[h][0] for h in h_list]
    tensor_list = [resolution_map[h][1] for h in h_list]
    time_index_list = [resolution_map[h][2] for h in h_list]
    filename_list = [resolution_map[h][3] for h in h_list]
    return positions_list,tensor_list,time_index_list,h_list,filename_list


def get_difference(positions,tensors):
    """
    Assumed that positions is a list of [position1,position2] and
    tensors is a list of [tensor1,tensor2]
    Returns a list of positions and tensors that is the difference
    between tensor1 and tensor2 at the courser positions
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
                difference.append(tensors[course_index][i] \
                                      - tensors[other_index][j])
    return pos,difference


def course_grain(fine_position,fine_tensor,course_position,course_tensor):
    """
    Takes a data set fine_position, fine_tensor and evaluates it only at
    the grid points where fine_position intersects fine_tensor. Returns
    positions and tensor values.
    """
    # Filtering requires lists
    course_grained_position = list(fine_position)
    course_grained_tensor = list(fine_tensor)
    # Now, go through fine_position and fine_tensor and delete any point
    # not in the intersection of fine_position and course_position
    for i in range(len(fine_position)):
        if fine_position[i] not in course_position:
            course_grained_position[i] = BAD_MARKER
            course_grained_tensor[i] = BAD_MARKER
    # Now actually delete the points
    course_grained_position = filter(FILTER_FUNCTION, course_grained_position)
    course_grained_tensor = filter(FILTER_FUNCTION, course_grained_tensor)
    return np.array(course_grained_position), np.array(course_grained_tensor)


def set_domain(position,tensor):
    """
    Ensures that the domain of the input data is correct. In other
    words, removes ghost points.
    """
    # Filtering requires lists
    my_position = list(position)
    my_tensor = list(tensor)
    # Go through it
    for i in range(len(my_position)):
        if not XMIN <= my_position[i] <= XMAX:
            my_position[i] = BAD_MARKER
            my_tensor[i] = BAD_MARKER
    # Delete the bad points
    my_position = filter(FILTER_FUNCTION,my_position)
    my_tensor = filter(FILTER_FUNCTION, my_tensor)
    return np.array(my_position),np.array(my_tensor)


def course_grain_all(positions,tensors):
    """
    course grains all data sets in positions, tensors.
    """
    # Ensure the list is ordered
    assert reduce(ANDFUNC, [len(positions[i]) < len(positions[i+1]) for i in range(len(positions)-1)]) and "The list must be ordered coursest to finest."
    # Some convenience names and ensure that the domain of the
    # course-grained solution is correct
    coursest_position,coursest_tensor=set_domain(positions[0],tensors[0])
    # Course grain everything
    course_positions = [coursest_position]
    course_tensors = [coursest_tensor]
    for i in range(len(tensors)-1):
        temp_pos,temp_tensor=course_grain(positions[1:][i],tensors[1:][i],
                                          coursest_position,
                                          coursest_tensor)
        course_positions.append(temp_pos)
        course_tensors.append(temp_tensor)
    # Ensure that all the course-grained data points are the same
    assert reduce(ANDFUNC,[len(course_positions[i]) == len(course_positions[i+1]) for i in range(len(course_positions)-1)]) and "All course-grained datasets must share the same x values"
    return coursest_position,course_tensors


def get_differences(tensors):
    """
    Generalizes get_difference. Takes a list of positions and a list
    of tensors of arbitrary length. Returns a new list of positions and
    differences. All datasets are compared to the most fine-grained
    data set.

    The points on which to compare are chosen by the most
    course-grained data set.

    It is assumed that sort_lists was called on these datasets.
    """
    # Compare to the finest-grained solution
    finest_tensor = tensors[-1]
    differences = []
    for tensor in tensors[:-1]:
        differences.append(tensor - finest_tensor)

    # And we're done!
    return differences


def find_order(differences,h_list):
    """
    Finds the order of convergence based on the differences calculated
    using get_differences.
    """
    # Some convenience names. We use the three finest-grain solutions
    d = differences[-2:]
    h = h_list[-3:]
    # We want to solve for n when this is zero
    func = lambda n: np.max(np.abs(d[1] - d[0] * ((h[0]**n - h[2]**n)/(h[1]**n - h[2]**n))**(-1)))
    xopt = fmin(func,N0)
    n = xopt[0]
    return n


def find_alpha(differences,h_list,n):
    """
    Find the factor that multiplies the lattice spacing to give an
    error. Requires a calculated value for n, the order of convergence.

    Each element of differences is assumed to by a numpy array.
    """
    return differences[-1]/(h_list[-2]**n - h_list[-1]**n)


def find_true_tensor(tensor,h,alpha,n):
    """
    Takes a course-grained tensor and the alpha and n calculated for
    it and uses it to find the true solution at the points the tensor
    is evaluated at.

    tensor and alpha are assumed to be numpy arrays.
    """
    return tensor - alpha * h**n


def output_tensor(position,tensor,filename):
    """
    Outputs tensor(position) as a two-column array to file named
    filename
    """
    with open(filename,'w') as f:
        for i in range(len(position)):
            f.write("{} {}\n".format(position[i],tensor[i]))
    return


def get_error_scale_factors(h_list,n):
    """
    Returns the vaues to scale differences so that they line
    up. Assumed the course-grained values are compared to the
    finest-grained value.
    """
    return [((h_list[i]**n - h_list[-1]**n)/(h_list[i+1]**n - h_list[-1]**n))**(-1) for i in range(len(h_list)-2)] + [1]


def plot_convergence(position,differences_list,h_list,n,time):
    """
    Plots the rescaled differences as a function of position. If they
    line up, we have self-convergence.

    h_list is the list of lattice spacings. n is the convergence
    coefficient. time is the time at which the data is evaluated. (PDE
    is hyperbolic.)
    """
    # Change the font size
    mpl.rcParams.update({'font.size':FONTSIZE})

    # Rescales the differences
    error_scale_factors = get_error_scale_factors(h_list,n)
    rescaled_differences = [error_scale_factors[i] * differences_list[i] for i in range(len(error_scale_factors))]

    # Define the plots
    lines = [plt.plot(position,difference,linewidth=LINEWIDTH) for difference in rescaled_differences]

    # Plot parameters
    plt.xlim([XMIN,XMAX])
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(PLOT_TITLE.format(time,n))
    plt.legend([LEGEND_TEMPLATE.format(h,h_list[-1]) for h in h_list[:-1]])
    plt.show()
    return            


def main(time,filename_list):
    """
    Takes a list of filenames and a time and performs Richardson
    extrapolation on the appropriate data at the appropriate
    time. Prints the convergence order to the terminal and saves the
    alpha and true solution datasets to separate files.
    """
    print "Welcome to the richardson extrapolation program."
    # Extract data
    print "Loading files..."
    positions_list,tensor_list,time_index_list,h_list=get_tensor_data(time,filename_list)
    # Sort lists
    print "Sorting lists..."
    positions_list,tensor_list,time_index_list,h_list,filename_list = sort_lists(positions_list,tensor_list,time_index_list,h_list,filename_list)
    # Get course grid points
    print "Generating course grid points..."
    course_positions,course_tensor_list = course_grain_all(positions_list,tensor_list)
    # Differences
    print "Getting the differences between data sets..."
    differences_list = get_differences(course_tensor_list)
    # Find convergence order
    print "Finding order of convergence..."
    n = find_order(differences_list,h_list)
    print "Order = {}".format(n)
    # Find the factor for error
    print "Finding contribution to error due to problem..."
    alpha = find_alpha(differences_list,h_list,n)
    print "Printing..."
    output_tensor(course_positions,alpha,ALPHA_FILE)
    # Find the true solution. Use finest grain solution for extrapolation
    print "Finding true solution..."
    true_solution = find_true_tensor(course_tensor_list[-1],h_list[-1],alpha,n)
    print "Printing..."
    output_tensor(course_positions,true_solution,TRUE_SOLUTION_FILE)
    # Plot
    print "Plotting convergence test..."
    plot_convergence(course_positions,differences_list,h_list,n,time)
    print "All done! Thanks!"
    return


if __name__ == "__main__":
    time = float(sys.argv[1])
    filename_list = sys.argv[2:]
    main(time,filename_list)
