import tkinter
import datetime
import numpy as np
import cv2 as cv
import pyautogui
import webbrowser


status = ""

#Find the time for name
def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name


#GUI
root = tkinter.Tk()
root.resizable(False, False)
root.title("Frame Recorder")
root.iconbitmap('record.ico')
root.geometry("800x400+500+100")
header = tkinter.Label(text="Frame Recorder", font=(None, 30))
create_label = tkinter.Label(text="Create an", font=(None, 20))
switch = tkinter.Scale(from_=100, to=200, orient=tkinter.HORIZONTAL, length=200)
video_label = tkinter.Label(text="fps video", font=(None, 20))

#Start button command
def create_vid():
    global out
    screen_size = pyautogui.size()
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    out = cv.VideoWriter("Outputs/FrameRecorder " + find_time() + ".avi", fourcc, switch.get(), (screen_size))

def record():
    img = pyautogui.screenshot()
    frame = np.array(img)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out.write(frame)

def start_record():
    create_vid()
    status_playing("playing")

#Report what's happening
def status_playing(yeter):
    global status
    status = yeter
    if status == "don":
        pause["state"] = "disabled"
        start["state"] = "normal"
        start.config(text="⏵ Play")
        info.config(text="Paused. Continue Recording with Play.")
    elif status == "playing":
        pause["state"] = "normal"
        end["state"] = "normal"
        start["state"] = "disabled"
        start.config(text="⏵ Play")
        info.config(text="Recording...")
    elif status == "end":
        info.config(text="Video Saved At Outputs Folder. Let's Create Another One!")
        pause["state"] = "disabled"
        end["state"] = "disabled"
        start["state"] = "normal"
        start.config(text="+ New")

start = tkinter.Button(text="⏵ Start", font=(None, 20), command=lambda :start_record())
pause = tkinter.Button(text="⏸ Pause", font=(None, 20), command=lambda :status_playing("don"))
end = tkinter.Button(text="⏹ End", font=(None, 20), command=lambda :status_playing("end"))
info = tkinter.Label(text="Start Recording", font=(None, 16))

#When started
end["state"] = "disabled"
pause["state"] = "disabled"

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))
watermark = tkinter.Label(root, text=r"https://github.com/mehmet-mert", fg="blue", cursor="hand2")
while True:
    root.update()
    header.place(x=400, y=20, anchor=tkinter.N)
    create_label.place(x=200, y=150, anchor=tkinter.CENTER)
    switch.place(x=400, y=146, anchor=tkinter.CENTER)
    video_label.place(x=600, y=150, anchor=tkinter.CENTER)

    start.place(x=200, y=250, anchor=tkinter.CENTER)
    pause.place(x=400, y=250, anchor=tkinter.CENTER)
    end.place(x=600, y=250, anchor=tkinter.CENTER)
    info.place(x=400, y=320, anchor=tkinter.CENTER)
    watermark.place(x=400, y=360, anchor=tkinter.CENTER)
    watermark.bind("<Button-1>", callback)
    if status == "playing":
        record()
    elif status == "don":
        pass
    elif status == "end":
        out.release()
