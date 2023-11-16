from datetime import datetime
import os
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
from time import sleep

from config import FOLDER_NAME, FILE_PREFIX, PICTURE_INTERVAL

SWITCH_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(SWITCH_PIN, GPIO.IN)

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)


def set_up_folder():
    folder_time = datetime.now().strftime("")
    if os.path.isdir(f"/home/astro/wearable_camera/{FOLDER_NAME}") ==  False:
        os.mkdir(f"/home/astro/wearable_camera/{FOLDER_NAME}")

    os.chdir(f"/home/astro/wearable_camera/{FOLDER_NAME}")

def run_camera():

    camera_is_running = True

    picam2.start()

    pic_counter = 0

    compare_time = datetime.now().strftime("%H%M")


    while camera_is_running == True:
        system_time = datetime.now().strftime("%H%M")

        if compare_time == system_time:
            pic_counter = pic_counter + 1
        else:
            pic_counter = 0

        compare_time = datetime.now().strftime("%H%M")

        picam2.capture_file(f"{FILE_PREFIX}{system_time}-{pic_counter}.jpg")
        print(f"{FILE_PREFIX}{system_time}-{pic_counter}.jpg")

        sleep(PICTURE_INTERVAL)

        if GPIO.input(SWITCH_PIN):
            camera_is_running = False


def exit_sequence():
    picam2.close()
    print("camera closed")
    exit()

if __name__ == "__main__":
    try:
        set_up_folder()

        while True:
            if GPIO.input(SWITCH_PIN) == False:
                run_camera()

        exit_sequence()

    except KeyboardInterrupt:
        exit_sequence()