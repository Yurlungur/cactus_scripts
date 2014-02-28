#!/usr/bin/env python2

"""
plot_robust_stability_evolution.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-02-28 15:01:25 (jonah)>

This little program plots the L2 norm of the (x,y)-component of the
3-metric of the Minkowski spacetime as a function of time. This is
very useful for the robust stability Apples-With-Apples test.

Example call:
python2 plot_robust_stability_evolution *.metric.norm2.asc
"""

# Imports
# ----------------------------------------------------------------------
import numpy as np # Array support
import sys # command line IO
# plot tools
import matplotlib as mpl
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
TIME_INDEX = 1 # index in numpy array for time
GXY_INDEX = 3 # index in numpy array for the (x,y)-component of the metric
LINEWIDTH=3
FONTSIZE=20
XLABEL = "Time"
YLABEL = r'$|g_{xy}|_2$'
TITLE = "Robust Stabiity Test Over Time"
# ----------------------------------------------------------------------

def main(filename_list):
    """
    Generates the plot from filename_list.
    """
    # Get the data
    data_sets = [np.loadtxt(filename).transpose() for filename in filename_list]
    # Set up the plot
    mpl.rcParams.update({'font.size':FONTSIZE})
    lines = [plt.plot(data[TIME_INDEX],data[GXY_INDEX],linewidth=LINEWIDTH) for data in data_sets]
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(TITLE)
    plt.legend(filename_list)
    plt.show()
    return

if __name__ == "__main__":
    main(sys.argv[1:])
