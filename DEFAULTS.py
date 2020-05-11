#   This file contains all the default settings objects used in the program
#   These are used when generating missing settings json files

MAIN_OBJ = {
    'self': 'mainSettings.json',
    'error': 'True',
    'FB_Enabled': 'True',
    'OCR_Setup': 'False',
    'Audio_Setup': 'False',
}

#   default ocr process settings
OCR_OBJ = {
    'self': 'OCRSettings.json',
    'fb_data_url': '/pi_test_status/ocr_status/',
    'fb_status_url': '/pi_test_status/ocr_status/',
    'running': 'False',
    'loopMode': 'infinite',
    'loopEnd': '',
    'srcImg': 'source.jpg',
}

OCR_DATA = {
    'self': 'OCRData.json',
    'dataset': {}
}

#   7 // ssd -> clock display
#   8 // eng -> single line of text

#   default OCR_DATA['dataset'] entry
OCR_DATA_ENTRY = {
    'name': 'crop1',
    'file': 'crop1.jpg',
    'psm': '7',
    'lang': 'ssd',
    'text': 'null'
}

#   default coordObj values -> used in CoordList / CoordObj
COORD_OBJ = {
    'name': 'null',
    'topL': (1, 1),
    'botR': (2, 2)
}

AUDIO_OBJ = {
    'self': 'audioSettings.json',
    'fb_data_url': '/pi_test_status/audio_status/audio_data/',
    'fb_status_url': '/pi_test_status/audio_status/',
    'running': 'False',
    'loopMode': 'infinite',
    'loopEnd': '',
    'refPath': 'reference.wav',
    'smplPath': 'sample.wav',
    'detected': 'Not Detected',
    'reference': 0,
}


#   List of all settings objects -> used when generating missing files
LIST_ALL = {
    'mainSettings.json': MAIN_OBJ,
    'OCRSettings.json': OCR_OBJ,
    'OCRData.json': OCR_DATA,
    'audioSettings.json': AUDIO_OBJ,
}

#   list of valid loop types
LOOP_TYPES = ['infinite', 'single', 'timed', 'press']
AUDIO_LOOP_TYPES = ['infinite', 'single', 'timed', 'press']
OCR_LOOP_TYPES = ['infinite', 'single', 'timed', 'press']

#   touchscreen dimensions
SCREEN_DIMS = {'width': 800, 'height': 480}


#   Files that must never be deleted
FORBIDDEN = ['kittens.jpg', 'smartnode_key.json', 'dependencies.txt']

FINGER_GPIO = 40