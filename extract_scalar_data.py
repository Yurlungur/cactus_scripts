"""
extract_scalar_data.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-07 23:21:27 (jonah)>

This is a library that extracts scalar data from the flattened array
of a scalar that's used in the Cactus ASCII gunuplot output mode.
----------------------------------------------------------------------

The goal is to extract information in a way that makes it easy to
plot. For example, to plot the x-component as a function of time at a
given position. This means we want a multidimensional array. The array
is based on machine time iteration. Then the format is

[snapshot1, snapshot2, snapshot3,...]

where each snapshot takes place at a different iteration.
The format of the snapshots is

[row1,row2,row3,row4,...],

where each row is a list of the form

[time_step, tl, [rl,c,ml], [ix,iy,iz], t, [x,y,z], data],

tl = time level. You can output past time levels if you store them,
i.e., if you use a multistep integrator. Or if you use adaptive mesh
refinement. Current time is zero. Past times are >= 1

rl = Refinement level. Adaptive mesh refinement. Course grid is level 0.

c = component. The index of the processor the domain is on.

ml = multigrid level. Unused. Always zero.

ix,iy, and iz are the indexes of the lattice points on the grid. Data
is the scalar data.
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # For arrays
# Relies heavily on the extract_tensor_data library for methods
import extract_tensor_data as etd 
# ----------------------------------------------------------------------

def extract_data(filename):
    """
    Extracts the data from a file and makes a list of snapshots as
    defined above in the approach.
    """
    return etd.extract_data(filename)

def get_lattice_spacing(data):
    """
    Extracts the grid spacing by measuring the 2-norm of the
    difference between two points in a given snapshot at a given
    time. The snapshot and time are assumed not to matter. This is
    obviously a poor assumption for adaptive mesh refinement and will
    need to be rethunk in more serious cases.
    """
    return etd.get_lattice_spacing(data)

def scalar_at_position_of_time(position,data):
    """
    Returns two lists, time and the scalar in dataset data at the
    position given by the position index. This is not a physical
    position. Instead it's the index in the snapshot. One-dimensional
    output should be a projection onto an axis or or a one-dimensional
    line. So these will naturally be in order.
    """
    times = []
    scalars = []
    for iteration in data:
        times.append(iteration[0][4])
        scalars.append(iteration[position][-1])
    times = np.array(times)
    scalars = np.array(elements)
    return times,scalars

def scalar_at_position_of_time_from_file(position,filename):
    """
    Same as scalar at position of time, but extracts information from
    a file.
    """
    data = extract_data(filename)
    return scalar_at_position_of_time(position,data)

def scalar_of_position_at_time(coord,time,data):
    """
    Returns two lists, position in the spacetime, and the scalar in
    dataset data at that position. Both are evaluated at the time
    given by time. This is number of computer iterations, not
    coordinate time.

    coord gives the coordinate to examine. 0=x,1=y,2=z
    """
    positions = []
    scalars = []
    for line in data[time]:
        positions.append(line[5][coord])
        scalars.append(line[-1])
    positions = np.array(positions)
    scalars = np.array(elements)
    return positions,scalars

def scalar_of_position_at_time_from_file(coord,time,filename):
    """
    Same as scalar of position at time, but extracts information from a file
    """
    data = extract_data(filename)
    return scalar_of_position_at_time(coord,time,data)

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

def scalar_difference_between_files(iteration1,iteration2
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
    data1 = extract_data(filename1)
    data2 = extract_data(filename2)
    return scalar_difference(iteration1,iteration2,data1,data2)


if __name__=="__main__":
    raise ImportWarning(etd.WARNING_MESSAGE)
