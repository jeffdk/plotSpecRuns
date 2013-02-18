"""
Functions and utilities for parsing spec runs
"""
import glob
import os
import operator


def parseRunDirNames(runBaseName):
    listOfRunDicts = []
    
    dirList = glob.glob(runBaseName + "*")

    #print dirList

    for thisDir in dirList:

        runDict = runDictFromDirName(thisDir)
        locateRunPortions(runDict)
        listOfRunDicts.append(runDict)
    print listOfRunDicts
    getlev = operator.itemgetter('grLev')
    print map(getlev, listOfRunDicts)
    return sorted(listOfRunDicts, key=getlev)


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

def locateRunPortions(runDict):
    """
    Searches directory of runDict for collapse & ringdown segments and adds information to runDict
    """

    segments = glob.glob(runDict['directory'] + '/*')
    assert segments, "Omg no run segments found in: %s" % runDict['directory']

    for segment in segments:
        if 'Ringdown' in segment:
            runDirectory = glob.glob(segment + '/Lev?/Run/')
            assert runDirectory, "No run directory found in Ringdown"
            assert len(runDirectory) < 2, "More than one run directory found in Ringdown!"
            runDict['ringdown'] = runDirectory[0]
        else:
            runDirectory = segment + '/Run/'
            assert os.path.exists(runDirectory), \
                "Run directory does not exist in collapse: %s" % runDirectory
            runDict['collapse'] = runDirectory

    return runDict