#!/usr/bin/env python2

"""
plot_gaugewave_multipatch_gxx.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-11 13:38:32 (jonah)>


This program plots the xx component of the metric for a gauge wave at
time t of every input file and compares it to the expected gaugewave.

We generate two plots. The first plot is the analytic gaugewave and
the solution gaugewave. The second is the error.

This version of the code is adapted for multipatch.

You pass the directory name of the simulation to the plot.

Example call:
python2 plot_gaugewave_multipatch_gxx.py 0 directory1 directory2 directory3
"""

# Imports
# ----------------------------------------------------------------------
import plot_gaugewave_multipatch as pg # library for plotting gaugewave tensors with multipatch
import numpy as np # For array support
import sys # for globbing support
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
YLABEL = r'$g_{xx}$'
# ----------------------------------------------------------------------

def gaugewave_gxx(x,t):
    """
    The analytic form of the gxx component of a gaugewave as a
    function of x,y,z and t, but projected along the x-axis. In other
    words, we set y=z=0.
    """
    y=0
    z=0
    A = (1.0/3.0)*pg.A
    #D = pg.D/np.sqrt(3.0)
    D = 3*pg.D/np.sqrt(3.0)
    return 1 + A*np.sin((2*np.pi*(3*t + np.sqrt(3.0)*(-x+y+z)))/D)

if __name__ == "__main__":
    pg.generate_it_all(gaugewave_gxx,sys.argv,YLABEL)
