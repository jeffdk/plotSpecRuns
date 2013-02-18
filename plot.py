"""
For plotting SpEC runs
"""
#import matplotlib
import os
import matplotlib.pyplot as plt
import numpy
from parsing import parseRunDirNames
from specRunClass import datFile, simulation
import h5py
import plot_defaults



runsDirectory = "/home/jeff/work/specRuns"
runSequenceName = "gam2TOV"


startingDirectory = os.getcwd()

##############################################################################
# Start analysis
##############################################################################
os.chdir(runsDirectory)


gam2TOV = simulation('gam2TOV')

lengths = []

##############################################
#Density convergence
##############################################
for i, run in enumerate(gam2TOV.listOfRunDicts):

    #print gam2TOV.runData['DensestPoint.dat'][i]['time']
    lengths.append( len(gam2TOV.runData['DensestPoint.dat'][i]['time']) )
#    plt.semilogy(gam2TOV.runData['DensestPoint.dat'][i]['time'],
#                 gam2TOV.runData['DensestPoint.dat'][i]['Rho0Phys'] )
# end = min(lengths )
# plt.semilogy(gam2TOV.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( gam2TOV.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - gam2TOV.runData['DensestPoint.dat'][1]['Rho0Phys'][1:end]  ))
# plt.semilogy(gam2TOV.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( gam2TOV.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - gam2TOV.runData['DensestPoint.dat'][1]['Rho0Phys'][1:end]  ))
# plt.semilogy(gam2TOV.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( gam2TOV.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - gam2TOV.runData['DensestPoint.dat'][2]['Rho0Phys'][1:end]  ))
# plt.show()

##############################################
# Waves
##############################################

for i, run in enumerate(gam2TOV.listOfRunDicts):

    print gam2TOV.wavesList[i]



##############################################################################
# Clean up
##############################################################################

os.chdir(startingDirectory)
