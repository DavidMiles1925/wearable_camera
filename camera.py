from picamera2 import Picamera2, Preview
from time import sleep
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

PICTURE_INTERVAL = 5

def exit_sequence():
    picam2.close()
    print("camera closed")
    exit()

if __name__ == "__main__":
    try:
        
        picam2.start()
        pic_counter = 1

        while True:

            system_time = datetime.now().strftime("%H%M")
            print(system_time)

            picam2.capture_file(f"{system_time}-{pic_counter}.jpg")
            print(f"{system_time}-{pic_counter}.jpg")

            sleep(PICTURE_INTERVAL)

            if pic_counter > (60/PICTURE_INTERVAL):
                pic_counter = 1
            else:
                pic_counter = pic_counter + 1

        exit_sequence()

    except KeyboardInterrupt:
        exit_sequence()