"""Giorgio: I2C communication to implement
x-y: up, down, left, right
z: up, down
"""
from pynput import keyboard
import cv2 as cv
from rasp_I2C_comms import *

root = ""


class Calibrate_Team:

    def __init__(self, num, team):
        self.num = num
        self.team = team
        self.file_loc = f"{root}//{team}"

    def start(self):
        print(f"starting calibration for team: {self.team}")
        # show the streamed video
        count = 0
        while count < self.num:
            print(f"\tcomponent: {count}, coordinate: {None}")
            # open camera
            # move to location specified
            move_to(0,0)
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            listener.join()
            count += 1
            # make frame
            # 
            # frame = None
            # cv.imwrite("{dir}//{i}.jpg", frame)


def on_press(key):
    if key == keyboard.Key.esc or key == keyboard.Key.enter:
        return False
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    key_dict = {"w":XY_up, "a": XY_left, "s": XY_down, "d": XY_right, "q": Z_up, "e": Z_down}
    if k.lower() in key_dict.keys():
        key_dict[k.lower()]()

    


team1 = Calibrate_Team(10,"1")

team1.start()




