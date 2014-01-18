#!/usr/bin/env python2

"""
tensor_self_convergence_test.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-01-16 12:15:34 (jonah)>

This is a program that runs a self convergence test on all input
files. It takes the difference of every file in the list with respect
to the last file in the list. Then it plots the the differences scaled
by the lattice spacing.

the syntax is:
python2 tensor_self_convergence_test.py time res1.asc res2.asc res3.asc

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
import sys
import numpy as np
import extract_tensor_data as etd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plot_gaugewave as pg
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
ACCEPTABLE_ERROR = 1E-14
PLOT_TITLE="Self Convergence Test at time t = {}"
XLABEL="Position"
YLABEL="Scaled Difference"
LEGEND_TEMPLATE = "h = {}"
XMIN=0
XMAX=1
# ----------------------------------------------------------------------

def sort_lists(positions_list,Txx_list,time_index_list,h_list,filename_list):
    """
    Takes a set of lists for data acquired by calling
    plot_gaugewave.get_Txx_data(time,filename_list) and sorts the lists
    based on the resolutions.
    """
    resolution_map = {h_list[i] : (positions_list[i], Txx_list[i], time_index_list[i], filename_list[i]) for i in range(len(h_list))}
    h_list.sort()
    h_list.reverse()
    positions_list = [resolution_map[h][0] for h in h_list]
    Txx_list = [resolution_map[h][1] for h in h_list]
    time_index_list = [resolution_map[h][2] for h in h_list]
    filename_list = [resolution_map[h][3] for h in h_list]
    return positions_list,Txx_list,time_index_list,h_list,filename_list

# def get_coursest_grid_points(positions_list):
#     """
#     Given a list of position arrays, returns a list of lists of
#     indices. These are the indices for which the position values match
#     up.
# 
#     It is assumed sort_lists has already been run so that the first
#     element of the positions list is the coarsest array.
#     """
#     index_lists = [[] for position_array in positions_list]
#     for i in range(len(positions_list[0])):
#         for j in range(len(positions_list)):
#             for k in range(len(positions_list[j])):
#                 if np.abs(positions_list[j][k] - positions_list[0][i]) < ACCEPTABLE_ERROR and k not in index_lists[j]:
#                     index_lists[j].append(k)
#     print index_lists
#     for i in index_lists:
#         print len(i)
#     return index_lists
# 
# def get_differences(positions_list,Txx_list,index_lists):
#     """
#     Finds the difference between the tensors at the shared course-grid
#     resolution sites. Outputs the difference and the positions as a
#     course-grid output.
# 
#     The last element of the differences_list output should be zero
#     since its the difference between the finest-grain file and itself.
# 
#     It is assumed that sort_lists and get_coursest_grid_points have
#     already been run.
#     """
#     positions = positions_list[0]
#     differences_list = [[] for i in Txx_list]
#     for i in range(len(index_lists)-1):
#         for j in range(len(index_lists[i])):
#             differences_list[i].append(- Txx_list[i][index_lists[i][j]] + Txx_list[i+1][index_lists[i+1][j]])
#     differences_list[-1] = [0 for i in range(len(index_lists[-1]))]
#     return positions,differences_list



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

def get_differences(positions_list

def scale_differences(differences_list,h_list):
    """
    Scales each difference array by the lattice spacing.
    """
    return [(h_list[i]**pg.EXPONENT)*differences_list[i]\
                for i in range(len(h_list))]

def plot_convergence(positions,differences_list,h_list,time):
    """
    Plots the rescaled differences. If they line up, we have
    self-convergence.
    """
    # Find the plot domain
    xmin = np.min(positions)
    xmax = np.max(positions)

    # Change the font size
    mpl.rcParams.update({'font.size': pg.fontsize})

    # Define plots
    lines = [plt.plot(positions,differences_list[i],linewidth=pg.my_linewidth)\
                 for i in range(len(differences_list))]
    
    # Plot parameters
    plt.xlim([xmin,xmax])
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(PLOT_TITLE.format(time))
    plt.legend([LEGEND_TEMPLATE.format(h) for h in h_list])
    plt.show()
    return

def main(time,filename_list):
    """
    Takes a list of filenames, extracts their data, finds and rescales
    the differences, and plots the self-convergence test.
    """
    # extract data
    positions_list,Txx_list,time_index_list,h_list=pg.get_Txx_data(time,filename_list)
    # sort lists
    positions_list,Txx_list,time_index_list,h_list,filename_list = sort_lists(positions_list,Txx_list,time_index_list,h_list,filename_list)
    # get course grid points
    for i in range(len(positions_list)):
        positions_list[i] = filter(lambda x: 0<=x<=1,positions_list[i])
    index_lists = get_coursest_grid_points(positions_list)
    # get differences and rescale
    positions,differences_list = get_differences(positions_list,
                                                 Txx_list,index_lists)
    differences_list = scale_differences(differences_list,h_list)
    # plot
    plot_convergence(positions,differences_list,h_list,time)
    return

if __name__ == "__main__":
    time = float(sys.argv[1])
    file_list = sys.argv[2:]
    main(time,file_list)
    
    
