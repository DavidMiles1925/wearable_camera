import RPi.GPIO as GPIO

SWITCH_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(SWITCH_PIN, GPIO.IN)

while True:
    if GPIO.input(SWITCH_PIN) == False:
        print("on")