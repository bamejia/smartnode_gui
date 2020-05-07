import DEFAULTS as defaults
from CoordList import coordList
from CoordObj import coordObj

tempObj = defaults.COORD_OBJ

tempList = coordList()

tempList.addObject(coordObj('testObj', (123, 123), (456, 456)))
tempList.popLast()

tempList.printSet()
