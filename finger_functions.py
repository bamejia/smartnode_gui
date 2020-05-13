import DEFAULTS as default

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)  # Set GPIO usage
    GPIO.setup(default.FINGER_GPIO, GPIO.OUT)  # Set up pin 32 for GPIO usage
    pwm = GPIO.PWM(default.FINGER_GPIO, 50)  # Set up pwm on pin 32

except ModuleNotFoundError:
    print("GPIO library not imported!")

# keeps multiple finger processes from occurring, since there is only one finger
can_finger_press = True

# minimum delay between finger movements
default_delay = 300

# stores tkinter after function
tkinter_after_func = lambda x, y, *z: 0


#####    Moves finger to starting, retracted position with value of 1
def startPos(next_func, data):
    print("in startPos")
    pwm.start(0)  # Set initial pwm of 0
    GPIO.setwarnings(False)  # Disable GPIO warnings
    GPIO.output(default.FINGER_GPIO, True)
    pwm.ChangeDutyCycle(2.055)

    tkinter_after_func(default_delay, pin_off, next_func, data)


#####    Moves finger to the press position with value of 50
def pressPos(next_func, data):
    print("in pressPos")
    pwm.start(0)  # Set initial pwm of 0
    GPIO.setwarnings(False)  # Disable GPIO warnings
    GPIO.output(default.FINGER_GPIO, True)
    pwm.ChangeDutyCycle(4.777)

    tkinter_after_func(default_delay, pin_off, next_func, data)


def pin_off(next_func, data):
    print("in pin_pff")
    GPIO.output(default.FINGER_GPIO, False)
    pwm.ChangeDutyCycle(0)
    if next_func == "start_pos":
        tkinter_after_func(data[0] - default_delay, startPos, 'check_loop', data)
    elif next_func == "press_pos":
        tkinter_after_func(data[0] - default_delay, pressPos, 'check_loop', data)
    elif next_func == "check_loop":
        delay, repeats, interval = data
        repeats -= 1
        tkinter_after_func(interval, finger_looper, delay, repeats, interval)


def cleanup():
    try:
        GPIO.cleanup()
    except NameError:
        print("unable to clean up GPIO")


# presses finger, holds it, and releases it according to input parameters
# push_hold has a minimum of 300ms
def finger_looper(*data):
    print("in finger_looper")

    global can_finger_press
    repeats = data[1]
    if repeats >= 0:
        pressPos("start_pos", data)
    else:
        can_finger_press = True


def finger_handler(*data):
    global can_finger_press
    if can_finger_press:
        can_finger_press = False
        finger_looper(*data)
    else:
        print("Cannot press finger that fast")


def set_after_function(after_func):
    global tkinter_after_func
    tkinter_after_func = after_func
