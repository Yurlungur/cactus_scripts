"""
extract_coordinates_data.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-06 12:58:38 (jonah)>

When the Coordinates thorn is active, the coordinates information in a
data file is incorrect and one must use the Grid::coordinates file to
map to the physical configuration space. This little library defines
the functions that do this.
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # For arrays
from numpy.linalg import norm # for grid spacing
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2
WARNING_MESSAGE = "This is a library. You are only supposed to import it!"
# ----------------------------------------------------------------------

def make_coordinate_maps(filename):
    """
    Extracts the data from a file and makes a list of snapshots,
    {snapshot1, snapshot2, snapshot3,...}
    where each snapshot takes place at a different iteration.
    Each snapshot is a list containing three dictionaries:
    [{ix:x}, {iy:y}, {iz:z}]
    which map grid coordinates to physical coordinates.
    """
    data = np.loadtxt(filename)
    snapshots = {int(line[0]) : [{},{},{}] for line in data}
    for row in data:
        # Convenience variable definitions
        time_step = int(row[0])
        tl = int(row[1])
        rl = int(row[2])
        c = int(row[3])
        ml = int(row[4])
        ix = int(row[5])
        iy = int(row[6])
        iz = int(row[7])
        t = row[8]
        x = row[9]
        y = row[10]
        z = row[11]
        true_x = row[12]
        true_y = row[13]
        true_z = row[14]
        r = row[15]
        snapshots[row[0]][0][ix]=true_x
        snapshots[row[0]][1][iy]=true_y
        snapshots[row[0]][2][iz]=true_z
    keys = snapshots.keys()
    keys.sort()
    snapshots_list = [snapshots[keys[i]] for i in range(len(keys))]
    return snapshots_list

def difference_stensil(my_list,my_index):
    """
    Finds the difference between my_list[my_index] and its neighboring
    elements. If the element has two neighbors, averages the
    difference.
    """
    assert 0 <= my_index < len(my_list)
    if my_index == 0:
        difference = norm(my_list[my_index+1] - my_list[my_index])
    elif my_index == len(my_list)-1:
        difference = norm(my_list[my_index] - my_list[my_index-1])
    else: # centered difference
        differences = norm(my_list[my_index+1] - my_list[my_index-1])/2.0
    return differences

def get_lattice_spacing(coordinate_maps,axis=X_AXIS):
    """
    In a general multipatch (or DGFE) system, the grid spacing is not
    fixed accross the entire space. Instead we need a continuous grid
    spacing. This function generates a grid spacing as a function of
    position and time.

    The output is a list where each entry corresponds to a
    snapshot. Each entry is a dictionary mapping x,y,or z to a lattice
    spacing, along that direction, depending on the choice of axis.

    This function is not guaranteed to work if the grid is not Cartesian.
    """
    
    spacing_snapshots = []
    for i in range(len(coordinate_maps)):
        positions = list(set(coordinate_maps[i][axis].values()))
        positions.sort()
        spacing_map = {positions[i] : difference_stensil(positions,i)\
                           for i in range(len(positions))}
        spacing_snapshots.append(spacing_map)
    return spacing_snapshots

def get_all_coord_data(filename,axis=X_AXIS):
    """
    Returns both coordinate maps and lattice spacing from a file
    """
    maps = make_coordinate_maps(filename)
    spacing = get_lattice_spacing(maps,axis)
    return maps,spacing

if __name__=="__main__":
    raise ImportWarning(WARNING_MESSAGE)
