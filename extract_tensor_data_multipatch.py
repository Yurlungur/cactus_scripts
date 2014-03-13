"""
extract_tensor_data_multipatch.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 10:29:59 (jonah)>

This little library extends extract_tensor_data.py to be multipatch aware.

It uses both the grid::coordinates files and the data files
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np
import extract_tensor_data as etd
import extract_coordinates_data as ecd
import simfactory_interface as interface
# ----------------------------------------------------------------------

# some simple wrappers
extract_data = etd.extract_data
make_coordinate_maps = ecd.make_coordinate_maps
WARNING_MESSAGE = etd.WARNING_MESSAGE

def sort_list_pair(list1,list2):
    """
    Sometimes two lists are coupled: the ith element of list1
    corresponds to the ith element of list2. Thus, if we want to sort
    list1, we must rearrange list2 so that it still matches list1.
    """
    list2D = {list1[i] : list2[i] for i in range(len(list1))}
    list1.sort()
    list2 = [list2D[i] for i in list1]
    return list1,list2
    
def element_of_position_at_snapshot(i,j,coord,snapshot,maps,time_index):
    """
    Returns two lists, position in the spacetime and the (i,j)th
    element of the tensor in the snapshot at that position.

    coord gives the coordinate to examine. 0=x,1=y=2=z

    Uses maps extracted from ecd.make_coordinate_maps

    time_index is the index of the snapshot.
    """
    positions = []
    elements = []
    for line in snapshot:
        positions.append(maps[time_index][coord][line[3][coord]])
        elements.append(etd.tensor_element(i,j,line[-1]))
    # positions and elements may not be sorted
    positions,elements = sort_list_pair(positions,elements)
    # Put them in numpy arrays for speed
    positions = np.array(positions)
    elements = np.array(elements)
    return positions,elements

def element_of_position_at_time(i,j,coord,time,data,maps):
    """
    Returns two lists, position in the spacetime, and the (i,j)th
    element of the tensor in dataset data at that position. Both are
    evaluated at the time given by time. This is number of computer
    iterations, not coordinate time.

    coord gives the coordinate to examine. 0=x,1=y=2=z

    Uses maps extracted from ecd.make_coordinate_maps
    """
    return element_of_position_at_snapshot(i,j,coord,data[time],maps,time)


if __name__=="__main__":
    raise ImportWarning(WARNING_MESSAGE)
