import numpy as np
import cv2 as cv
import pyautogui
import datetime
import locale

#Kullanıcıya göre dil değiştirme
if locale.getdefaultlocale()[0] == "tr_TR":
    fps = int(input("Videonuz kaç fps'de oluşturulsun(20-80):"))
else:
    fps = int(input("How many fps to create video(20-80):"))

#Video adlandırması için tarih bulma
def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name

#Videoyu oluşturma
screen_size = (1920, 1080)
fourcc = cv.VideoWriter_fourcc(*"XVID")
out = cv.VideoWriter("Outputs/FrameRecorder " + find_time() + ".avi", fourcc, fps, (screen_size))

if locale.getdefaultlocale()[0] == "tr_TR":
    print("Video başladı, işiniz bittiği zaman 'q' ya basıp çıkabilirsiniz.")
else:
    print("Video started, when you done open video window and press 'q")

#Videoyu çekme
while True:
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out.write(frame)
    cv.imshow("Show", frame)
    if cv.waitKey(1) == ord("q"):
        break
