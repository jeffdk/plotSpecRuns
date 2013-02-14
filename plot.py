"""
For plotting SpEC runs
"""
#import matplotlib
import os
import matplotlib.pyplot as mpl
from parsing import parseRunDirNames


mpl.rc('text', usetex=True)
mpl.rc('font', family='serif')
font = {'size': 24}
mpl.rc('font', **font)
mpl.rc('axes', labelsize='large')

runsDirectory = "/home/jeff/work/specRuns"
runSequenceName = "tovOctSym"


startingDirectory = os.getcwd()

##############################################################################
# Start analysis
##############################################################################
os.chdir(runsDirectory)

listOfRunDicts = parseRunDirNames(runSequenceName)


print listOfRunDicts










##############################################################################
# Clean up
##############################################################################

os.chdir(startingDirectory)
