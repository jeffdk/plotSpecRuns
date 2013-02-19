"""
For plotting SpEC runs
"""
import matplotlib
import os
import matplotlib.pyplot as plt
from specRunClass import datFile, simulation
import plot_defaults



runsDirectory = "/home/jeff/work/specRuns"
startingDirectory = os.getcwd()

##############################################################################
# Start analysis
##############################################################################
os.chdir(runsDirectory)
runString = 'gam2D4'
simToPlot = simulation(runString)
lengths = []
#print runString.split('gam2')[1]
plt.text(.85,.70,runString.split('gam2')[1])
##############################################
#Density convergence
##############################################
for i, run in enumerate(simToPlot.listOfRunDicts):

    #print simToPlot.runData['DensestPoint.dat'][i]['time']
    lengths.append( len(simToPlot.runData['DensestPoint.dat'][i]['time']) )
#    plt.semilogy(simToPlot.runData['DensestPoint.dat'][i]['time'],
#                 simToPlot.runData['DensestPoint.dat'][i]['Rho0Phys'] )
# end = min(lengths )
# plt.semilogy(simToPlot.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( simToPlot.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - simToPlot.runData['DensestPoint.dat'][1]['Rho0Phys'][1:end]  ))
# plt.semilogy(simToPlot.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( simToPlot.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - simToPlot.runData['DensestPoint.dat'][1]['Rho0Phys'][1:end]  ))
# plt.semilogy(simToPlot.runData['DensestPoint.dat'][i]['time'][1:end],
#              numpy.abs( simToPlot.runData['DensestPoint.dat'][0]['Rho0Phys'][1:end]
#              - simToPlot.runData['DensestPoint.dat'][2]['Rho0Phys'][1:end]  ))
# plt.show()
##############################################
# Baryon mass/symmetry factor convergence
##############################################

# legendList=[]
# matplotlib.rcParams['figure.subplot.left'] = 0.18
# for i, run in enumerate(simToPlot.listOfRunDicts):
#
#     if run['grLev'] > 2:
#         legendList.append('Lev'+str(i)+' - Lev'+ str(i-1))
#         plt.plot(simToPlot.runData['RestMass.dat'][i]['time'],
#                  simToPlot.runData['RestMass.dat'][i]['mass']
#                  -simToPlot.runData['RestMass.dat'][i-1]['mass'] )
#
# lg = plt.legend(legendList, loc=2)
# lg.draw_frame(False)
# plt.xlabel(r"$time_{(code)}$")
# plt.ylabel(r"$\delta M_b$")
# plt.show()

##############################################
# lapse
##############################################

legendList=[]
for i, run in enumerate(simToPlot.listOfRunDicts):

    if run['grLev'] == 3:
        legendList.append('Gauge = ' + str(run['gauge']))
        plt.plot(simToPlot.runData['MinLapse.dat'][i]['time'],
                 simToPlot.runData['MinLapse.dat'][i]['Min(Lapse)'])

lg = plt.legend(legendList, loc=1)
lg.draw_frame(False)
plt.xlabel(r"$time_{(code)}$")
plt.ylabel(r"min( $\alpha$ )")
plt.show()

##############################################
# Constraints
###############################################

legendList=[]
matplotlib.rcParams['figure.subplot.left'] = 0.18
for i, run in enumerate(simToPlot.listOfRunDicts):
    simToPlot.runData['Constraints/GhCe.dat'][i].removeDuplicateTimesteps()
    if True:
        legendList.append('GrLev = ' + str(run['grLev']) + ',  Gauge = ' + str(run['gauge']))
    #if run['gauge'] == 'full':
    #    legendList.append('GrLev = ' + str(run['grLev']))
    #if run['grLev'] == 4:
    #    legendList.append('Gauge = ' + str(run['gauge']))
        plt.semilogy(simToPlot.runData['Constraints/GhCe.dat'][i]['time'],
                 simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCe)']
                 / simToPlot.runData['Constraints/GhCe.dat'][i]['VolLp(GhCeDenom)'])

lg = plt.legend(legendList, loc=2)
lg.draw_frame(False)

plt.xlabel(r"$time_{(code)}$")
plt.ylabel(r"$L_2$ norm of GhCe")
plt.show()



##############################################
# Densest point
###############################################

legendList=[]
matplotlib.rcParams['figure.subplot.left'] = 0.18
for i, run in enumerate(simToPlot.listOfRunDicts):

    if run['grLev'] == 3:
        legendList.append('Gauge = ' + str(run['gauge']))
        plt.semilogy(simToPlot.runData['DensestPoint.dat'][i]['time'],
                 simToPlot.runData['DensestPoint.dat'][i]['Rho0Phys'])

lg = plt.legend(legendList, loc=2)
lg.draw_frame(False)

plt.xlabel(r"$time_{(code)}$")
plt.ylabel(r"max $\rho_{b,\,(code)}$ ")
plt.show()



##############################################
# SqrtDetG
##############################################

legendList=[]
for i, run in enumerate(simToPlot.listOfRunDicts):
    #print simToPlot.runData['MinMaxOfSqrtDetg.dat'][i].getCols()
    #0
    #h5py.Dataset().attrs
    if run['grLev'] == 3:
        legendList.append('Gauge = ' + str(run['gauge']))
        plt.semilogy(simToPlot.runData['MinMaxOfSqrtDetg.dat'][i]['time'],
                 simToPlot.runData['MinMaxOfSqrtDetg.dat'][i]['Max(SqrtDetg)'])

lg = plt.legend(legendList, loc=2)
lg.draw_frame(False)
plt.xlabel(r"$time_{(code)}$")
plt.ylabel(r"max($\sqrt{g})$")
plt.show()


##############################################
# Waves
##############################################
r = 100
matplotlib.rcParams['figure.subplot.left'] = 0.2
legendList=[]
for i, run in enumerate(simToPlot.listOfRunDicts):

    #0
    #h5py.Dataset().attrs
    #print simToPlot.wavesList[i]['rd'].keys()
    if run['grLev'] < 5 and run['gauge'] == 'full':
        legendList.append('GrLev=' + str(run['grLev']))
        plt.plot(simToPlot.wavesList[i]['rd']['R0'+str(r)+'.dir']['Y_l2_m0.dat'][:,0],
                 simToPlot.wavesList[i]['rd']['R0'+str(r)+'.dir']['Y_l2_m0.dat'][:,1])
        # plt.plot(simToPlot.wavesList[i]['rd']['R0063.dir']['Y_l2_m2.dat'][:,0],
        #          simToPlot.wavesList[i]['rd']['R0063.dir']['Y_l2_m2.dat'][:,1])
plt.figtext(.85,.20,runString.split('gam2')[1],size=24)
lg = plt.legend(legendList)
lg.draw_frame(False)
plt.xlabel(r"$time_{(code)}$")
plt.ylabel(r"$Re[ r\Psi_4 ]^2_2$ \,  r="+str(r))
plt.show()



##############################################################################
# Clean up
##############################################################################

os.chdir(startingDirectory)
