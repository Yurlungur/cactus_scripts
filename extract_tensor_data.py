"""
extract_tensor_data.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-01 22:12:41 (jonah)>

This is a library extracts the data from the flattened array of a
tensor that's used in Cactus ASCII gnuplot output.
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
is for a 3x3 symmetric tensor

[Txx, Txy, Txz, Tyy, Tyz, Tzz]

where T is whatever tensor we're interested in. Since the tensor is
symmetric, this is all the information.
"""
# ----------------------------------------------------------------------


# Imports
# ----------------------------------------------------------------------
import numpy as np # For arrays
from numpy.linalg import norm
# ----------------------------------------------------------------------


# Global variables
# ----------------------------------------------------------------------
WARNING_MESSAGE = "This is a library. You are only supposed to import it!"
# ----------------------------------------------------------------------

def find_largest_index_of_subvalue(collection, value):
    """
    Finds the index of the largest element in the collection less than
    value.
    """
    subcollection = filter(lambda x: x <= value, collection)
    return collection.index(max(subcollection))

def to_array_or_float(input_string,separator=' '):
    """
    Takes an input string and makes it a float if it's one
    number. Otherwise makes it a numpy array.
    """
    if len(input_string.split(separator)) == 1:
        return eval(input_string.rstrip())
    else:
        return np.fromstring(input_string.rstrip(),dtype=float,sep=separator)

def get_string(filename):
    """
    Takes a file name string as input and returns the file as one big
    long string.
    """
    with open(filename) as f:
        file_data = f.read()
    return file_data

def get_iterations(filestring):
    """
    Takes a string received by get_string and splits it into blocks
    based on time step in the cactus iteration.
    """
    return filter(lambda x: bool(x), filestring.split('\n\n\n'))

def make_iteration_subarray(iter_string):
    """
    Takes a string which is one element of the list generated by
    get_iterations, and generates a multidimensional subarray
    """
    # First mak the iter string into a list of space-separated lists.
    # We also remove the comment lines.
    list_strings = filter(lambda x: bool(x) and x[0] != '#',
                          iter_string.split('\n'))
    # We now split by tabs and turn grouped elements into 1d arrays
    # and lone elements into floating-point numbers.
    data = [[to_array_or_float(column.rstrip()) \
                 for column in row.split('\t')] \
                for row in list_strings]
    # That's it. We're done!
    return data

def lose_ghost_points(snapshot):
    """
    A snapshot at a given iteration is likely to contain ghost
    points. We don't want to double count these. This method removes
    the ghost points.
    """
    # We iterate through each row in the snapshot. If the position in
    # that row is in the positions set, we delete that row. Otherwise,
    # we add the positions to the positions set.
    positions = []
    for i in range(len(snapshot)):
        if list(snapshot[i][3]) in positions:
            snapshot[i] = False
        else:
            positions.append(list(snapshot[i][3]))
    snapshot = filter(lambda row: bool(row), snapshot)
    return snapshot

def extract_data(filename):
    """
    Extracts the data from a file and makes a list of snapshots as
    defined above in the approach.
    """
    data_string = get_string(filename)
    iterations = [lose_ghost_points(make_iteration_subarray(iteration)) \
                      for iteration in get_iterations(data_string)]
    return iterations

def get_lattice_spacing(data):
    """
    Extracts the grid spacing by measuring the 2-norm of the
    difference between two points in a given snapshot at a given
    time. The snapshot and time are assumed not to matter. This is
    obviously a poor assumption for adaptive mesh refinement and will
    need to be rethunk in more serious cases.
    """
    position1 = data[0][0][5]
    position2 = data[0][1][5]
    spacing = norm(position2 - position1)
    return spacing

def tensor_element(i,j,tensor):
    """
    tensor is a 6-element numpy array that represents a symmetric
    3x3 tensor.

    tensor_element extracts the (i,j)th element of tensor.
    """
    assert 0 <= i < 3 and 0 <= j < 3 and "We're working with a 3x3 tensor."
    if i == 0:
        return tensor[j]
    elif i == 1 and j == 1:
        return tensor[3]
    elif i == 1 and j == 2:
        return tensor[4]
    elif i == 2 and j == 2:
        return tensor[5]
    else:
        return tensor_element(j,i,tensor)

def element_at_position_of_time(i,j,position,data):
    """
    Returns two lists, time and the (i,j)th element of the tensor in
    dataset data at the position given by the position index. This is
    not a physical position. Instead it's the index in the
    snapshot. One-dimensional output should be a projection onto an
    axis or or a one-dimensional line. So these will naturally be in
    order.
    """
    times = []
    elements = []
    for iteration in data:
        times.append(iteration[0][4])
        elements.append(tensor_element(i,j,iteration[position][-1]))
    times = np.array(times)
    elements = np.array(elements)
    return times,elements

def element_at_position_of_time_from_file(i,j,position,filename):
    """
    Same as element at position of time, but extracts information from
    a file.
    """
    data = extract_data(filename)
    return element_at_position_of_time(i,j,position,data)

def element_of_position_at_time(i,j,coord,time,data):
    """
    Returns two lists, position in the spacetime, and the (i,j)th
    element of the tensor in dataset data at that position. Both are
    evaluated at the time given by time. This is number of computer
    iterations, not coordinate time.

    coord gives the coordinate to examine. 0=x,1=y=2=z
    """
    positions = []
    elements = []
    for line in data[time]:
        positions.append(line[5][coord])
        elements.append(tensor_element(i,j,line[-1]))
    positions = np.array(positions)
    elements = np.array(elements)
    return positions,elements

def element_of_position_at_time_from_file(i,j,coord,time,filename):
    """
    Same as element_of_position_at_time but extracts information from
    a file.
    """
    data = extract_data(filename)
    return element_of_position_at_time(i,j,coord,time,data)

if __name__=="__main__":
    raise ImportWarning(WARNING_MESSAGE)
