import numpy as np
import cv2 as cv
import pyautogui
import datetime

def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name

fps = int(input("How many fps to create video(20-80):"))

screen_size = (1920, 1080)
fourcc = cv.VideoWriter_fourcc(*"XVID")
out = cv.VideoWriter("Outputs/FrameRecorder " + find_time() + ".avi", fourcc, fps, (screen_size))
print("Video started, when you done open video window and press 'q")
while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out.write(frame)
    cv.imshow("Show", frame)
    if cv.waitKey(1) == ord("q"):
        break
