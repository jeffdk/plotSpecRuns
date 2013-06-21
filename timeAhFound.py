"""
For plotting SpEC runs
"""
import matplotlib
import os
import matplotlib.pyplot as plt
from specRunClass import datFile, simulation
import plot_defaults



runsDirectory = "/home/jeff/work/specRuns/"
startingDirectory = os.getcwd()

##############################################################################
# Start analysis
##############################################################################
os.chdir(runsDirectory)
runString = 'tov-'
simToPlot = simulation(runString)
lengths = []

ahFound = {'shift': 1,
           'full': 1,
           'harm': 0,
           'slice': 1,
           'froze': 0}
colors = ['b','g','r','c','m']
##############################################
# Constraints
###############################################

legendList=[]
plertList = []
matplotlib.rcParams['figure.subplot.left'] = 0.18
colorIndex = -1
for i, run in enumerate(simToPlot.listOfRunDicts):

    simToPlot.runData['Constraints/GhCe.dat'][i].removeDuplicateTimesteps()
    if run['grLev'] == 3:
        legendList.append('Gauge = ' + str(run['gauge']))
        colorIndex += 1
    #if run['gauge'] == 'full':
    #    legendList.append('GrLev = ' + str(run['grLev']))
    #if run['grLev'] == 4:
    #    legendList.append('Gauge = ' + str(run['gauge']))
        plert, =plt.semilogy(simToPlot.runData['Constraints/GhCe.dat'][i]['time'],
                 simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCe)']
                 / simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCeDenom)'],
                 c=colors[colorIndex])
        plertList.append(plert)
        if ahFound[run['gauge']]:
             plt.semilogy(simToPlot.runData['Constraints/GhCe.dat'][i]['time'][-1],
             simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCe)'][-1]
             / simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCeDenom)'][-1], marker='o',
         ms=10, c=colors[colorIndex])
        else:
            plt.semilogy(simToPlot.runData['Constraints/GhCe.dat'][i]['time'][-1],
            simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCe)'][-1]
            / simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCeDenom)'][-1], marker='x',
            ms=10, c=colors[colorIndex])

lg = plt.legend(plertList, legendList, loc=2)
lg.draw_frame(False)

#plt.xlabel(r"$time_{(code)}$")
plt.xlabel(r"$t \,\,\, \mathrm{[code]}$")
plt.ylabel(r"$L_2$ norm of GhCe")
plt.show()



os.chdir(startingDirectory)
