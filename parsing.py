"""
Functions and utilities for parsing spec runs
"""
import glob


def parseRunDirNames(runBaseName):
    listOfRunDicts = []
    
    dirList = glob.glob(runBaseName + "*")

    print dirList

    for thisDir in dirList:
        listOfRunDicts.append(runDictFromDirName(thisDir))
    
    return listOfRunDicts


def runDictFromDirName(dirName):
    """
    Creates run information dictionary from dir name, e.g:
     input:  'tovOctSym-full-sL1fDX300pd0.8'
     output: {'directory': 'tovOctSym-full-sL1fDX300pd0.85', 'grLev': 1,
              'depletion': 0.85, 'gauge': 'full', 'hydroDx': 300.0}
    """
    runDict = dict(directory=dirName)

    runDict['gauge'] = dirName.split('-')[1]
    resolutionAndDepletion = dirName.split('-')[2]

    #Get spectral level
    resolutionAndDepletion = resolutionAndDepletion.split('sL')[1]
    resolutionAndDepletion = resolutionAndDepletion.split('fDX')
    runDict['grLev'] = int(resolutionAndDepletion[0])

    #Get hydro DX and pressure depletion
    resolutionAndDepletion = resolutionAndDepletion[1].split('pd')
    runDict['hydroDx'] = float(resolutionAndDepletion[0])
    runDict['depletion'] = float(resolutionAndDepletion[1])

    return runDict