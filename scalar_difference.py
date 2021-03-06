#!/usr/bin/env python2

"""
scalar_difference.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-13 22:00:45 (jonah)>

This program calculates and prints the difference between two scalar
files used in the cactus ASCII gnuplot output.

The call is
python2 scalar_difference.py iteration1 iteration2 simulation1 simulation2

where iteration1 and iteration2 are the computer time iterations where
we compare the scalars saved in the simulation files simulation1 and
simulation2.

The user can also set the optional flag abs using --abs anywhere in
the command after scalar_difference.py to tell the computer to
calculate the absolute value of the difference. This is often useful.

You can also set the flag --max or --min so that the program
calculates the maximum or the minimum of the difference and prints
it. This can be combined with ABS to calculate the maximum of the
absolute value of the difference.

Example call:
python2 scalar_difference.py --abs 0 0 simulation1.lapse.x.asc simulation2.lapse.x.asc 
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # for array support
import extract_scalar_data as esd
import sys # For UI
from copy import copy
# ----------------------------------------------------------------------

# Constants
# ----------------------------------------------------------------------
HEADER_INFO = """# Iteration1 = {}, Time1 = {}
# Iteration2 = {}, Time2 = {}
# column format: it   tl    [rl c ml]   [ix iy iz]  time  [x y z]  data"""
# ----------------------------------------------------------------------

# User flags
# ----------------------------------------------------------------------
ABS = False
MAX = False
MIN = False
FLAG_PREFIX='--'
ABS_FLAG='{}abs'.format(FLAG_PREFIX)
MAX_FLAG='{}max'.format(FLAG_PREFIX)
MIN_FLAG='{}min'.format(FLAG_PREFIX)
POSSIBLE_FLAGS = set([ABS_FLAG,MAX_FLAG,MIN_FLAG])
# ----------------------------------------------------------------------

# User interface
# ----------------------------------------------------------------------
def set_flags_and_prune_argvs(argvs):
    """
    Takes the list of user arguments sys.argv[1:] and prunes it to
    remove user flags and to set user flags internally.    
    """
    global ABS
    global MAX
    global MIN
    PRUNE_VALUE = "PRUNED"
    for i in range(len(argvs)):
        arg = argvs[i]
        if FLAG_PREFIX in arg:
            if arg == ABS_FLAG:
                 ABS = True
            elif arg == MAX_FLAG:
                 MAX = True
            elif arg == MIN_FLAG:
                MIN = True
            else:
                raise IOError("The flag {} is not valid.".format(arg))
            argvs[i] = PRUNE_VALUE
    return filter(lambda x: x != PRUNE_VALUE, argvs)
# ----------------------------------------------------------------------

def scalar_difference(iteration1,iteration2,data1,data2):
    """
    Takes two simulation datasets and generates an array that is the
    difference between the scalars in the first file and the second
    file at the given iterations. (Iteration here indexes snapshot
    number.)

    Iteration1 is the snapshot index for data1. Iteration2 is the
    snapshot index for data2.

    USE AT YOUR OWN RISK. VERY LIKELY TO FAIL UNLESS THE SIMULATIONS
    THE FILES ARE FOR HAVE EXACTLY THE SAME NUMBER OF GRID POINTS
    """
    scalar1 = np.array([row[-1] for row in data1[iteration1]])
    scalar2 = np.array([row[-1] for row in data2[iteration2]])
    assert len(scalar1) == len(scalar2), "Simulations have same number of grid points."
    return scalar1 - scalar2

def scalar_difference_between_files(iteration1,iteration2,
                                    filename1,filename2):
    """
    Takes two simulation files and generates an array that is the
    difference between the scalars in the first file and the second
    file at the given iteration. (Iteration here indexes snapshot
    number.)

    Iteration1 is the snapshot index for filename1. Iteration2 is the
    snapshot index for filename2.

    USE AT YOUR OWN RISK. VERY LIKELY TO FAIL UNLESS THE SIMULATIONS
    THE FILES ARE FOR HAVE EXACTLY THE SAME NUMBER OF GRID POINTS
    """
    data1 = esd.extract_data(filename1)
    data2 = esd.extract_data(filename2)
    return scalar_difference(iteration1,iteration2,data1,data2)

def print_difference(iteration1,iteration2,filename1,filename2):
    """
    Prints the difference between the data at iteration1 in filename1
    and at iteration2 in filename 2 as an array. Also prints the
    appropriate data for coordinates of the field given in the rest of
    the snapshot. This information comes from filename 1 and is
    assumed to be the same.
    """
    data1 = esd.extract_data(filename1)
    data2 = esd.extract_data(filename2)
    time1 = data1[iteration1][0][4]
    time2 = data2[iteration2][0][4]
    difference = scalar_difference(iteration1,iteration2,data1,data2)
    if ABS:
        difference = np.abs(difference)
    print HEADER_INFO.format(iteration1,time1,iteration2,time2)
    for i in range(len(data1[iteration1])):
        outlist = copy(data1[iteration1][i])
        outlist[-1] = "{0:.17f}".format(difference[i])
        outstring = reduce(lambda x,y: "{} {}".format(x,y), outlist)
        print outstring
    return

def print_extremal_difference(iteration1,iteration2,filename1,filename2):
    """
    Prints either the maximum or the minimum difference between the
    data at iteration1 in filename1 and at iteration2 in filename 2.
    """
    difference = scalar_difference_between_files(iteration1,iteration2,
                                                 filename1,filename2)
    if ABS:
        difference = np.abs(difference)
    if MAX:
        print "{0:.17f}".format(np.max(difference))
    elif MIN:
        print "{0:.17f}".format(np.min(difference))
    else:
        raise ValueError("Neither the max nor min flag is set.")

if __name__ == "__main__":
    argvs = set_flags_and_prune_argvs(copy(sys.argv[1:]))
    iteration1 = int(argvs[0])
    iteration2 = int(argvs[1])
    filename1 = argvs[2]
    filename2 = argvs[3]
    if MAX or MIN:
        print_extremal_difference(iteration1,iteration2,filename1,filename2)
    else:
        print_difference(iteration1,iteration2,filename1,filename2)

