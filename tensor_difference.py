#!/usr/bin/env python2

"""
tensor_difference.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-13 22:35:04 (jonah)>

This program calculates and prints the difference between two tensor
files used in the cactus ASCII gunuplot output.

The call is
python2 tensor_difference.py iteration1 iteration2 simulation1 simulation2

where iteration1 and iteration2 are the computer time iterations where
we compare the scalars saved in the simulation files simulation1 and
simulation2.

Example call:
python2 scalar_difference.py 0 0 simulation1.shift.x.asc simulation2.shift.x.asc 
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # for array support
import extract_tensor_data as etd
import sys #for UI
from copy import copy
# ----------------------------------------------------------------------

# Constants
# ----------------------------------------------------------------------
HEADER_INFO = """# Iteration1 = {}, Time1 = {}
# Iteration2 = {}, Time2 = {}
# column format: it   tl    [rl c ml]   [ix iy iz]  time  [x y z]  data"""
# ----------------------------------------------------------------------

def tensor_difference(iteration1,iteration2,data1,data2):
    """
    Takes two simulation datasets and generates an array that is the
    difference between the tensors in the first file and the second
    file at the given iterations. (Iteration here indexes snapshot
    number.)

    Iteration1 is the snapshot index for data1. Iteration2 is the
    snapshot index for data2.

    USE AT YOUR OWN RISK. VERY LIKELY TO FAIL UNLESS THE SIMULATIONS
    THE FILES ARE FOR HAVE EXACTLY THE SAME NUMBER OF GRID POINTS
    """
    tensor1 = [row[-1] for row in data1[iteration1]]
    tensor2 = [row[-1] for row in data2[iteration2]]
    difference = [tensor1[i] - tensor2[i] for i in range(len(tensor1))]
    return difference

def tensor_difference_between_files(iteration1,iteration2,
                                    filename1,filename2):
    """
    Takes two simulation files and generates an array that is the
    difference between the tensors in the first file and the second
    file at the given iteration. (Iteration here indexes snapshot
    number.)

    Iteration1 is the snapshot index for filename1. Iteration2 is the
    snapshot index for filename2.

    USE AT YOUR OWN RISK. VERY LIKELY TO FAIL UNLESS THE SIMULATIONS
    THE FILES ARE FOR HAVE EXACTLY THE SAME NUMBER OF GRID POINTS
    """
    data1 = etd.extract_data(filename1)
    data2 = etd.extract_data(filename2)
    return tensor_difference(iteration1,iteration2,data1,data2)

def print_difference(iteration1,iteration2,filename1,filename2):
    """
    Prints the difference between the data at iteration1 in filename1
    and at iteration2 in filename 2 as an array. Also prints the
    appropriate data for coordinates of the field given in the rest of
    the snapshot. This information comes from filename 1 and is
    assumed to be the same.
    """
    data1 = etd.extract_data(filename1)
    data2 = etd.extract_data(filename2)
    time1 = data1[iteration1][0][4]
    time2 = data2[iteration2][0][4]
    difference = tensor_difference(iteration1,iteration2,data1,data2)
    print HEADER_INFO.format(iteration1,time1,iteration2,time2)
    for i in range(len(data1[iteration1])):
        outlist = copy(data1[iteration1][i])
        outlist[-1] = "{}".format(np.max(np.abs(difference[i])))
        outstring = reduce(lambda x,y: "{} {}".format(x,y), outlist)
        print outstring
    return

if __name__ == "__main__":
    iteration1 = int(sys.argv[1])
    iteration2 = int(sys.argv[2])
    filename1 = sys.argv[3]
    filename2 = sys.argv[4]
    print_difference(iteration1,iteration2,filename1,filename2)
