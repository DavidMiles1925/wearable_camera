from datetime import datetime
import os
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
from time import sleep

from config import SAVE_DIRECTORY, FOLDER_NAME, FILE_PREFIX, PICTURE_INTERVAL

SWITCH_PIN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(SWITCH_PIN, GPIO.IN)

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)


def set_up_folder():
    folder_time = datetime.now().strftime("%d.%m.%Y")

    path_str = f"{SAVE_DIRECTORY}{FOLDER_NAME}{folder_time}"
    
    if os.path.isdir(path_str) ==  False:
        os.mkdir(path_str)

    os.chdir(path_str)

def run_camera(pic_counter):

    camera_is_running = True

    picam2.start()

    while camera_is_running == True:
        system_time = datetime.now().strftime("%H:%M")

        pic_counter_str = add_zeros_to_number(pic_counter)

        file_name = f"{FILE_PREFIX}-{pic_counter_str}-[{system_time}].jpg"

        picam2.capture_file(file_name)
        print(file_name)

        sleep(PICTURE_INTERVAL)

        if GPIO.input(SWITCH_PIN):
            camera_is_running = False
        
        pic_counter = pic_counter + 1


def add_zeros_to_number(num):
    num_str = str(num)

    num_zeros = 6 - len(num_str)

    if num_zeros > 0:
        return '0' * num_zeros + num_str
    else:
        return num_str
    

def exit_sequence():
    picam2.close()
    print("camera closed")
    exit()

if __name__ == "__main__":
    try:
        pic_counter = 0

        number_with_zeros = add_zeros_to_number(12)
        print(number_with_zeros)

        set_up_folder()

        while True:
            if GPIO.input(SWITCH_PIN) == False:
                run_camera(pic_counter)

    except KeyboardInterrupt:
        exit_sequence()