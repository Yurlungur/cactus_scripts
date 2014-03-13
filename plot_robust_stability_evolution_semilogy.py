#!/usr/bin/env python2

"""
plot_robust_stability_evolution_semilogy.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-13 11:39:21 (jonah)>

The same as plot_robust_stability_evolution.py, but plots the y-axis
on a log scale.

Example call:
python2 plot_robust_stability_evolution_semilogy.py directory1 directory2
"""

# Imports
# ----------------------------------------------------------------------
import plot_robust_stability_evolution
import sys
# ----------------------------------------------------------------------

PLOT_LOG = True

if __name__ == "__main__":
    plot_robust_stability_evolution.main(sys.argv[1:],PLOT_LOG)
