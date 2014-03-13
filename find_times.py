#!/usr/bin/env python2

"""
find_times.py
Author: Jonah Miller (jonah.maxwell.miller@gmail.com)
Time-stamp: <2014-03-12 12:25:05 (jonah)>

This little script looks at the data files in a directory for a
simulation and extracts at what coordinate times the simulation output
data.

It can look at any number of simulations at a time.

example call:
python2 find_times.py directory1 directory2 directory3
"""

# Imports
# ----------------------------------------------------------------------
import sys         # For globbing support
import numpy as np # For array support and fast file-reading
import re          # Regular expressions
import os          # Operating system interface
import simfactory_interface as interface
# ----------------------------------------------------------------------

# Global constants
# ----------------------------------------------------------------------
# Regular expression syntax for the file types we'll allow.
ALLOWED_FILE_TYPES = ['norm'+r'\S*','minimum','maximum']
ALLOWED_FILE_REGEX_STRINGS = [r'\S*'+'.'+i+interface.ASCII_POSTFACTOR\
                                  for i in ALLOWED_FILE_TYPES]
ALLOWED_FILE_REGEXES = [re.compile(i) for i in ALLOWED_FILE_REGEX_STRINGS]
# A formatting parameter. How far apart lists are.
FILLSIZE=22 # Should be set to the approximate size of directory names
FORMATSTRING="{:{fill}{align}{fillsize}}" # Used to format directory names
RESTART_NUMBER = interface.RESTART_NUMBER # = 0
# ----------------------------------------------------------------------

def combine_names(x,y):
    """
    Takes two names, x and y, and combines them into a single string
    that's nicely formatted.
    """
    return (FORMATSTRING+' '+FORMATSTRING).format(x,y,
                                              fill=" ",
                                              align="<",
                                              fillsize=FILLSIZE)

def access_maybe(index,L):
    """
    If 0 <= index <= len(L)-1, returns L[index]. Otherwise, returns an
    empty string.
    """
    if 0 <= index <= len(L) - 1:
        return L[index]
    else:
        return ""

def get_time_data(directory_name):
    """
    Given a directory name, extracts data from any one of the scalar
    output files and from it extracts timing information.
    """
    data_directory=interface.get_data_directory(directory_name,RESTART_NUMBER)
    for filename in os.listdir(data_directory):
        matches = [regex.match(filename) for regex in ALLOWED_FILE_REGEXES]
        # If nothing matches, evaluates to None. Otherwise evaluates
        # to one of the matching strings in the list. Which one is
        # unknown, but it doesn't matter.
        matching_string = max(matches) 
        if matching_string:
            break
    if not matching_string: # Then there were no matches at all
        raise IOError("There are no 1d files to open in directory\n\t"+directory_name)
    filepath = data_directory.rstrip('/') + '/' + matching_string.group(0)
    data = np.loadtxt(filepath).transpose()
    iterations = data[0]
    times = data[1]
    return times

def output_time_data(list_of_directories):
    """
    Given a list of directory names, finds the time data in each and
    outputs all times available for each file and then the
    intersections.
    """
    print "Extracting time data..."
    times = {directory : get_time_data(directory)\
                 for directory in list_of_directories}
    most_times = max([len(time) for time in times.values()])
    print most_times
    print "----------------------------------------------------------------"
    print "Time data for all directories"
    print "----------------------------------------------------------------"
    print reduce(combine_names, times.keys())
    for i in range(most_times):
        print reduce(combine_names,[access_maybe(i,times[k]) for k in times.keys()])
    print "----------------------------------------------------------------"
    print "The times that intersect:"
    intersections = list(reduce(lambda x,y: set(x) & set(y), times.values()))
    intersections.sort()
    for i in intersections:
        print "\t" + str(i)
    print "----------------------------------------------------------------"
    return
    
if __name__ == "__main__":
    output_time_data(sys.argv[1:])
            
