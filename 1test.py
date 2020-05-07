import json

import DEFAULTS as defaults

tempObj = defaults.COORD_OBJ
path = 'coordFile.json'
with open(path, 'w') as myFile:
    myFile.write(json.dumps(list(tempObj)))
