# tempObj = defaults.COORD_OBJ
# path = 'coordFile.json'
# with open(path, 'w') as myFile:
#     myFile.write(json.dumps(list(tempObj)))

from collections import deque

import DEFAULTS as defaults

test = defaults.LOOP_TYPES
options = deque()

for a in test:
    options.appendleft(a)
