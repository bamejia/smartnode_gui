import RPi.GPIO as GPIO
from time import sleep
import DEFAULTS as default


default_delay = 300


GPIO.setmode(GPIO.BOARD)  # Set GPIO usage
GPIO.setup(default.FINGER_GPIO, GPIO.OUT)  # Set up pin 32 for GPIO usage
pwm = GPIO.PWM(default.FINGER_GPIO, 50)  # Set up pwm on pin 32


#####    Moves finger to starting, retracted position with value of 1
def startPos(next_func, data):
    print("in startPos")
    # GPIO.setmode(GPIO.BOARD)  # Set GPIO usage
    # GPIO.setup(32, GPIO.OUT)  # Set up pin 32 for GPIO usage
    # pwm = GPIO.PWM(32, 50)  # Set up pwm on pin 32
    pwm.start(0)  # Set initial pwm of 0
    GPIO.setwarnings(False)  # Disable GPIO warnings
    GPIO.output(default.FINGER_GPIO, True)
    pwm.ChangeDutyCycle(2.055)

    data[0](default_delay, pin_off, next_func, data)

    # return int(delay * 1000)

    # sleep(0.5)
    # GPIO.output(32, False)
    # pwm.ChangeDutyCycle(0)
    # GPIO.cleanup()


#####    Moves finger to the press position with value of 50
def pressPos(next_func, data):
    print("in pressPos")
    # GPIO.setmode(GPIO.BOARD)  # Set GPIO usage
    # GPIO.setup(32, GPIO.OUT)  # Set up pin 32 for GPIO usage
    # pwm = GPIO.PWM(32, 50)  # Set up pwm on pin 32
    pwm.start(0)  # Set initial pwm of 0
    GPIO.setwarnings(False)  # Disable GPIO warnings
    GPIO.output(default.FINGER_GPIO, True)
    pwm.ChangeDutyCycle(4.777)

    data[0](default_delay, pin_off, next_func, data)

    # return int(delay * 1000)
    # sleep(0.5)
    # GPIO.output(32, False)
    # pwm.ChangeDutyCycle(0)
    # GPIO.cleanup()


def pin_off(next_func, data):
    print("in pin_pff")
    GPIO.output(default.FINGER_GPIO, False)
    pwm.ChangeDutyCycle(0)
    if next_func == "start_pos":
        data[0](data[2] - default_delay, startPos, 'check_loop', data)
    elif next_func == "press_pos":
        data[0](data[2] - default_delay, pressPos, 'check_loop', data)
    elif next_func == "check_loop":
        delay_func, set_finger_press, delay, repeats, interval = data
        repeats -= 1
        delay_func(interval, finger_looper, delay_func, set_finger_press, delay, repeats, interval)


def cleanup():
    GPIO.cleanup()


# presses finger, holds it, and releases it according to input parameters
# push_hold has a minimum of 300ms
def finger_looper(*data):
    print("in finger_looper")
    repeats = data[3]
    if repeats >= 0:
        pressPos("start_pos", data)
    else:
        data[1](True)

