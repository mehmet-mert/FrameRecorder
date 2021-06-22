import datetime    
import webbrowser
import interface
import tkinter      #for Linux you must install tkinter and scrot

import numpy as np  #pip install numpy
import cv2 as cv    #pip install opencv-python
import pyautogui    #pip install PyAutoGUI

status = ""


# Find the time for name
def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name


def edit_checks(clicked):
    if clicked == "mp4":
        if interface.mp4_format.get() == False:
            interface.avi_format.set(True)
        else:
            interface.avi_format.set(False)
    elif clicked == "avi":
        if interface.avi_format.get() == False:
            interface.mp4_format.set(True)
        else:
            interface.mp4_format.set(False)


def result_format():
    if interface.mp4_format.get() == True:
        return ".mp4"
    else:
        return ".avi"

def result_format2():
    if result_format() == ".mp4":
        return "MP4V"
    else:
        return "XVID"


interface.video_format.add_checkbutton(label=".mp4", onvalue=1, offvalue=0, variable=interface.mp4_format,
                                       command=lambda: edit_checks("mp4"))
interface.video_format.add_checkbutton(label=".avi", onvalue=1, offvalue=0, variable=interface.avi_format,
                                       command=lambda: edit_checks("avi"))

interface.about.add_command(label="Mehmet Mert Altuntas",
                            command=lambda: webbrowser.open("https://github.com/mehmet-mert"))


# Start button command
def create_vid():
    global out
    screen_size = pyautogui.size()
    fourcc = cv.VideoWriter_fourcc(*result_format2())
    out = cv.VideoWriter("Outputs/FrameRecorder " + find_time() + result_format(), fourcc, interface.switch.get(),
                         (screen_size))


def record():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out.write(frame)


def start_record():
    if status in ("end"):
        create_vid()
    status_playing("playing")


# Report what's happening
def status_playing(yeter):
    global status
    status = yeter
    if status == "stopped":
        interface.pause["state"] = "disabled"
        interface.start["state"] = "normal"
        interface.canvas.itemconfig(interface.info, text="Paused. Continue Recording with Play")
    elif status == "playing":
        interface.pause["state"] = "normal"
        interface.end["state"] = "normal"
        interface.start["state"] = "disabled"
        interface.canvas.itemconfig(interface.info, text="Recording...")
    elif status == "end":
        interface.canvas.itemconfig(interface.info, text="Video Saved At Outputs Folder. Let's Create Another One!")
        interface.pause["state"] = "disabled"
        interface.end["state"] = "disabled"
        interface.start["state"] = "normal"


interface.start.config(command=lambda: start_record())
interface.end.config(command=lambda: status_playing("end"))
interface.pause.config(command=lambda: status_playing("stopped"))

#interface.root.protocol("WM_DELETE_WINDOW", on_closing)
interface.running = True
while interface.running:
    interface.root.update()
    interface.switch.place(x=400, y=176, anchor=tkinter.CENTER)
    interface.start.place(x=318, y=230, width=172, height=58)
    interface.pause.place(x=118, y=230, width=172, height=58)
    interface.end.place(x=518, y=230, width=172, height=58)
    interface.root.config(menu=interface.menubar)
    if status == "playing":
        record()
    elif status == "stopped":
        pass
    elif status == "end":
        out.release()
