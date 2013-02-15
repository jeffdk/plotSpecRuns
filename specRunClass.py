import numpy


class simulation(object):

    ghceL2 = None
    ghceLinf = None

    def __init__(self,runsBase):
        assert isinstance(runsBase, str)


class datFile(object):

    columnHeaders = []
    dataTable = []
    observerName = ""
    def __init__(self, filename):
        assert isinstance(filename, str)

        filehandle = open(filename,'r')

        self.parse(filehandle)

    def parse(self, filehandle):

        gotObserverName = False

        for i, line in enumerate(filehandle):
            line = line.lstrip()

            #Comments in file start with a '#'
            if line[0]=='#':
                print line
                if not gotObserverName:
                    self.observerName = (line.lstrip(' # ')).strip()
                    gotObserverName = True
                    continue

            #TODO: check column numbers
                colHeader = line.split('=')[1].strip()
                self.columnHeaders.append(colHeader)
            else:
                entry = [float(value) for value in line.split()]
                assert len(entry) == len(self.columnHeaders), \
                    "Data line has different number of entries than column header!"
                self.dataTable.append(entry)
        self.dataTable = numpy.array(self.dataTable)
        print 'observerName, ', self.observerName
        print self.dataTable
