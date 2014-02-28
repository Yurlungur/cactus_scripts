VISUALIZATION SCRIPTS FOR APPLES-WITH-APPLES TESTS
======================================================================

Authors: Jonah Miller (jonah.maxwell.miller@gmail.com)
	 Frederico Guercilena
         Ian Hinder
	 Erik Schnetter

Time-stamp: <2014-02-28 15:15:47 (jonah)>

This is a suite of python scripts and mathematica notebooks to plot
the gaugewave, shifted gaugewave, and robust stability
Apples-with-Apples tests. Each file has documentation in a comment at
the top. This readme file exists to give the user a brief overview of
the suite's capabilities.

The scripts serve the following purposes:

extract_tensor_data.py:
                       --- This is not really a script. Rather, it's a library
		           of methods used to convert Cactus ASCII output into
			   Python data types. At the moment, it can
			   only extract one-dimensional data for symmetric
			   three-tensors projected along the x-axis.

extract_scalar_data.py:
                       --- Exactly the same as extract_tensor_data.py,
		           but for scalar information.

plot_gaugewave.py:
                       --- The final library in this set of scripts,
		           plot_gaugewave.py defines the methods to actually
			   plot a gaugewave solution. It also defines methods
			   to plot a convergence test if given an analytic
			   solution.
			   If you want to change parameters like the amplitude
			   or period of the gaugewave, you need to change
			   the constants at the top of this library for
			   the plot to come out right.

plot_gaugewave_*.py:
		       --- These little scripts are small wrappers of
		           plot_gaugewave.py that provide an analytic solution
			   to plot against. The plot the xx-component of the
			   metric or extrinsic curvature at a given time t
			   as function of space. One and 3d solutions available.
			   Available scripts:
			   --- plot_gaugewave_kxx.py
			   --- plot_gaugewave_gxx.py
			   --- plot_gaugewave_3d_gxx.py
			   Example call:
			   python2 /path/to/plot_gaugewave_kxx.py 0 rho2.curv.x.asc rho4.curv.x.asc
			   more documentation available in the mathematica notebook:
			   --- 3d_gaugewave_analysis.nb

plot_shifted_gaugewwave_*.py:
                       --- Same as plot_gaugewave_*.py, but for the shifted
		       	   gaugewave. More documentation available in the
			   following mathematica notebooks:
			   --- Shifted Gauge Wave Solution and Convergence.nb
			   --- 3d_shifted_gaugewave_analysis.nb
			   Available scripts:
			   --- plot_shifted_gaugewave_kxx.py
			   --- plot_shifted_gaugewave_3d_kxx.py

richardson_extrapolation.py:
                       --- Performs a richardson extrapolation on a set of
		       	   solutions to solve for the order
		           of convergence. Plots a convergence
			   test and outputs an ascii file with the true
			   solution. More documentation is available in
			   the pdf compiled from:
			   --- richardson_extrapolation.py
			   Example call:
			   python2 richardson_extrapolation.py time res1.asc res2.asc res3.asc

plot_robust_stability_at_time.py:
                       --- The robust stability test simulates a noisy Minkowski
		       	   space, so the off-diagonal components of the metric
			   should be zero. This means that a good approximation
			   of the error is the (x,y)-component of the metric. This
			   plots that component at a given time t as a function of
			   space projected along the x-axis. Useful for getting
			   a good idea of the simulations.
			   Example call:
			   python2 plot_robust_stability_at_time.py 0 rho2.metric.x.asc rho4.metric.x.asc

plot_robust_stability_evolution.py:
                       --- The robust stability test simulates a noisy Minkowski
		       	   space, so the off-diagonal components of the metric
			   should be zero. This means that a good approximation
			   of the total error is the L2-norm of the
			   (x,y)-component of the metric. This plots that for any
			   number of output files.
			   Example call:
			   python2 plot_robust_stability_evolution.py *.metric.norm2.asc
