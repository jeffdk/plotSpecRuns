import h5py
import os
import numpy
from parsing import parseRunDirNames


class simulation(object):
    """
    Storage scheme is:
    Ordered list of basic run information from filenames: listOfRunDicts
    Dictionary of lists of datFile objects, where the lists correspond to runs (as above)
     and the dictionary keys are the names of the data file filenames
    """
    ghceL2 = None
    ghceLinf = None

    densestPoint = None
    runData = None
    listOfRunDicts = None
    filesToParse = ('Constraints/GhCe.dat',
#                    '/Constraints/GhCeLinf.dat',
                    'DensestPoint.dat',
                    'MinMaxOfSqrtDetg.dat',
                    'MinLapse.dat',
                    'RestMass.dat')
    wavesList = None
    def __init__(self,runsBase):
        assert isinstance(runsBase, str)
        
        self.listOfRunDicts = parseRunDirNames(runsBase)
        print self.listOfRunDicts
        #print self.listOfRunDicts

        self.ghceL2 = []
        self.densestPoint = []
        self.runData = {key: [] for key in self.filesToParse }

        self.wavesList = []
        for run in self.listOfRunDicts:

            for currentFile in self.filesToParse:
                currentDatFile = datFile(run['collapse'] + currentFile)

                if 'ringdown' in run:
                    currentDatFile.appendDataFromFile(run['ringdown'] + currentFile)
                else:
                    #assert False, "NO RINGDOWN FOR %s" % run
                    pass
                self.runData[currentFile].append(currentDatFile)
                #print currentDatFile.getCols()
            #Do wave ext separately
            h5dict = None
            #HACKY NO RINGDOWN HACK TODO:FIX
            if 'ringdown' in run:
                h5dict = self.loadWaves(run['collapse'], run['ringdown'])
            else:
                h5dict = self.loadWaves(run['collapse'], run['collapse'])
                del h5dict['rd']
            self.wavesList.append(h5dict)

            #break
    def loadWaves(self, pathCollapse, pathRingdown):

        filename = "WaveExt/rPsi4_FiniteRadii_CodeUnits.h5"
        assert os.path.exists(pathCollapse + filename)
        assert os.path.exists(pathRingdown + filename)
        return {'cl': h5py.File(pathCollapse + filename, 'r'),
                'rd': h5py.File(pathRingdown + filename, 'r')}
        pass


class datFile(object):

    columnHeaders = None
    dataTable = None
    observerName = ""
    segmentBoundaries = None   # list of times at start of new segments
    def __init__(self, filename):
        assert isinstance(filename, str)

        self.columnHeaders = []
        self.dataTable = []
        self.segmentBoundaries = []
        self.observerName = None
        self.parse(filename)

    def __getitem__(self, key):

        for i, columnLabel in enumerate(self.columnHeaders):
            if key == columnLabel:
                return numpy.array(zip(*self.dataTable)[i])

        raise IndexError

    def getCols(self):
        return self.columnHeaders

    def hackNoColumnDatfiles(self,filename):
        """
        If a dat file in your simulation does not contain headers, define them here
        Input a filename, checks if dat file is a part of filename, returns column headers list
        """
        hackFilesDict= {'RestMass.dat': ['time', 'mass'],
                        }
        for key in hackFilesDict.keys():
            if key in filename:
                return hackFilesDict[key]

        return []



    #TODO: parse and appendDataFrom file need to be refactored to remove code duplication
    def parse(self, filename):

        filehandle = open(filename,'r')
        #print filename
        gotObserverName = False

        #check if a no-column dat file
        self.columnHeaders = self.hackNoColumnDatfiles(filename)

        for i, line in enumerate(filehandle):
            line = line.lstrip()

            #Comments in file start with a '#'
            if line[0] == '#':
                #print line
                if not gotObserverName:
                    self.observerName = (line.lstrip(' # ')).strip()
                    gotObserverName = True
                    continue

            #TODO: check column numbers
                colHeader = line.split('=')[1].strip()
                self.columnHeaders.append(colHeader)
            else:
                entry = [float(value) for value in line.split()]
                #print entry, self.columnHeaders
                assert len(entry) == len(self.columnHeaders), \
                    "Data line has different number of entries than column header!"
                self.dataTable.append(entry)
        self.dataTable = numpy.array(self.dataTable)
        #print 'observerName, ', self.observerName
        #print self.dataTable

        filehandle.close()


    def appendDataFromFile(self, filename):
        if not os.path.exists(filename) :
            print "Serious fucking warning: %s does not exist; not appending to data" % filename
            return

        filehandle = open(filename,'r')

        gotObserverName = False
        observerName = None
        gotFirstTstep = False
        firstTstep = None
        #check if a no-column dat file
        columnHeaders = self.hackNoColumnDatfiles(filename)
        dataTable=[]

        for i, line in enumerate(filehandle):
            line = line.lstrip()

            #Comments in file start with a '#'
            if line[0]=='#':
                #print line
                if not gotObserverName:
                    observerName = (line.lstrip(' # ')).strip()
                    gotObserverName = True
                    continue
                     #TODO: check column numbers
                colHeader = line.split('=')[1].strip()
                columnHeaders.append(colHeader)
            else:
                entry = [float(value) for value in line.split()]
                #print entry, self.columnHeaders
                assert len(entry) == len(columnHeaders), \
                    "Data line has different number of entries than column header!"
                if not gotFirstTstep:
                    for j, row in enumerate(entry):
                        if columnHeaders[j] == 'time':
                            firstTstep = row
                            gotFirstTstep = True
                            break

                dataTable.append(entry)
        #print 'fsttstep: ', firstTstep
        self.segmentBoundaries.append(firstTstep)
        dataTable = numpy.array(dataTable)
        print observerName,  self.observerName
        assert columnHeaders == self.columnHeaders, "Appending file doesn't match column headers!"
        assert observerName == self.observerName, "Appending file observer name doesn't match!"

        #print self.dataTable
        self.dataTable = numpy.vstack((self.dataTable, dataTable))
        #print
        #print self.dataTable
        filehandle.close()