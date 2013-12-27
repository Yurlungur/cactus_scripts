#!/usr/bin/env python2

"""
find_crash_point.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2013-12-27 02:59:40 (jonah)>
----------------------------------------------------------------------

The goal is to find an obvious and catastrophic crash of a simulation
in the Einstein Toolkit. Takes in a one-dimensional ascii output file
for a symmetric tensor. Outputs the file name and the time one
iteration before the system crashed. This isn't the iteration when it
crashes. This is coordinate time. A call might look like:

python2 find_crash_point.py *curv.x.asc

and output would look like

gaugewave.curv.x.asc 10 static_tov.curv.x.asc 3.63
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # for nan and arrays
import extract_tensor_data as etd # to deal with tensor ascii files
import sys # For globbing
# ----------------------------------------------------------------------

def abs_max(tensor):
    """
    Finds the maximum absolute value of a symmetric tensor.
    """
    return np.max(np.abs(tensor))

def bad_tensor(tensor):
    """
    Returns true if the tensor has diverged in any component.
    """
    t_max = abs_max(tensor)
    return t_max == np.nan or t_max == np.inf

def bad_snapshot(snapshot):
    """
    Returns true if a snapshot as defined in extract_tensor_data.py
    contains a bad tensor.
    """
    for row in snapshot:
        tensor = row[-1]
        if bad_tensor(tensor):
            return True
    return False

def get_time(data,iteration):
    """
    Given a computer time step and the data, finds the coordinate time.
    """
    return data[iteration][0][4]

def main(filename):
    """
    Takes a filename and finds the time right before the system
    crashed.
    """
    data = etd.extract_data(filename)

    for iteration in range(len(data)):
        if bad_snapshot(data[iteration]):
            print "{} {}".format(filename,get_time(data,iteration-1))
            return
    print "{} {}".format(filename, get_time(data,len(data)-1))
    return

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        main(filename)
    
