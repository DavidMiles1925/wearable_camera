from picamera2 import Picamera2, Preview
from time import sleep
from datetime import datetime
import os

from config import FOLDER_NAME, FILE_PREFIX, PICTURE_INTERVAL

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)




def set_up_folder():
    if os.path.isdir(f"/home/astro/wearable_camera/{FOLDER_NAME}") ==  False:
        os.mkdir(f"/home/astro/wearable_camera/{FOLDER_NAME}")

    os.chdir(f"/home/astro/wearable_camera/{FOLDER_NAME}")

def run_camera():

    picam2.start()

    pic_counter = 0

    compare_time = datetime.now().strftime("%H%M")


    while True:
        system_time = datetime.now().strftime("%H%M")

        if compare_time == system_time:
            pic_counter = pic_counter + 1
        else:
            pic_counter = 0

        print(system_time)
        print(pic_counter)

        picam2.capture_file(f"{FILE_PREFIX}{system_time}-{pic_counter}.jpg")
        print(f"{system_time}-{pic_counter}.jpg")

        sleep(PICTURE_INTERVAL)

        compare_time = datetime.now().strftime("%H%M")


def exit_sequence():
    picam2.close()
    print("camera closed")
    exit()

if __name__ == "__main__":
    try:
        set_up_folder()

        run_camera()

        exit_sequence()

    except KeyboardInterrupt:
        exit_sequence()