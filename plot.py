"""
For plotting SpEC runs
"""
#import matplotlib
import os
import matplotlib.pyplot as mpl
from parsing import parseRunDirNames
from specRunClass import datFile
import h5py

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


datFile('tovOctSym-full-sL1fDX300pd0.85/Lev0/Run/Constraints/GhCe.dat')

print listOfRunDicts

h5file = h5py.File('tovOctSym-full-sL1fDX300pd0.85/Lev0/Run/WaveExt/WaveExtraction.h5', 'r')


dset = h5file.get('rPsi4')




##############################################################################
# Clean up
##############################################################################

os.chdir(startingDirectory)
