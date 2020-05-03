#   This file contains all the default settings objects used in the program
#   These are used when generating missing settings json files

MAIN_OBJ = {
            'self': 'mainSettings.json',
            'error': 'True',
            'FB_Enabled': 'True',
            'OCR_Setup': 'False',
            'Audio_Setup': 'False',
            'OCR_Active': 'False',
            'Audio_Active': 'False'
            }

OCR_OBJ = {
            'self': 'OCRSettings.json',
            'fb_url': 'filler_audio_url',
            'loopMode': 'single',
            'loopEnd': '',
            'srcImg': 'source.jpg',
            'cropImgs': {'crop1': 'crop1.jpg'},
            'cropPSM': {'crop1': '7'},
            'cropLang': {'crop1': 'ssd'},
            'cropTxt': {'crop1': ''}

}

AUDIO_OBJ = {
            'self': 'audioSettings.json',
            'fb_url': 'filler_audio_url',
            'loopMode': 'single',
            'loopEnd': '',
            'refPath': 'reference.wav',
            'smplPath': 'sample.wav',
            'detected': 'False',
            'reference': 0,
}

FB_OBJ = {
            'self': 'firebaseSettings.json',
            'connected': 'False',
            'msg_from_fb': 'NOT_YET_IMPLEMENTED',
            'msg_to_fb': '',
            'msg_dest_url': ''
}

#   Not used yet, not sure why I made this...
GUI_OBJ = {
            'self': 'guiSettings.json',
            'stopRequest': 'False',
            'msg_to_GUI': ''
}

#   List of all settings objects -> used when generating missing files
LIST_ALL = {
            'mainSettings.json': MAIN_OBJ,
            'OCRSettings.json': OCR_OBJ,
            'audioSettings.json': AUDIO_OBJ,
            'firebaseSettings.json': FB_OBJ,
            'guiSettings.json': GUI_OBJ,
}

#   list of valid loop types
LOOP_TYPES = {'infinite', 'single', 'timed'}

#   touchscreen dimensions
SCREEN_DIMS = {'width': 800,    'height': 480 }