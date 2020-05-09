import collections

import DEFAULTS as defaults


def next_mode(current_mode):
    myDeque = collections.deque(defaults.AUDIO_LOOP_TYPES)
    index = myDeque.index(current_mode)
    myDeque.rotate(-1)
    return myDeque[index]
