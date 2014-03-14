#!/usr/bin/env python2

"""
plot_gaugewave_multipatch_gxx_error_of_time.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 13:05:50 (jonah)>


This program plots the xx component of the metric for a gauge wave as
a function of time for input directory and compares it to the expected
gaugewave.

Example call:
python2 plot_gaugewave_multipatch_gxx_error_of_time.py directory1 directory2
"""

# Imports
# ----------------------------------------------------------------------
import plot_gaugewave_norm2_error
import plot_gaugewave_multipatch as pg
import numpy as np # For array support
import sys # for globbing support
# ----------------------------------------------------------------------


# Global constants
# ----------------------------------------------------------------------
YLABEL = r'$g_{xx}$'
PLOT_SEMILOGY=False
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
    plot_gaugewave_norm2_error.main(gaugewave_gxx,sys.argv,PLOT_SEMILOGY)
