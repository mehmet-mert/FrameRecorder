import tkinter
from tkinter import *
import datetime
import numpy as np
import cv2 as cv
import pyautogui
import webbrowser

status = ""


# Find the time for name
def find_time():
    x = datetime.datetime.now()
    date_for_name = (x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y") + "-" + x.strftime("%H") + "-" +
                     x.strftime("%M") + "-" + x.strftime("%S"))
    return date_for_name


# GUI
root = tkinter.Tk()
root.resizable(False, False)
root.title("Frame Recorder")
root.geometry("800x400+500+100")
canvas = Canvas(root, bg="#4392F1", height=400, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
background_img = PhotoImage(file=f"assets/background.png")
background = canvas.create_image(400.0, 200.0, image=background_img)
header = canvas.create_text(400.0, 91.0, text="Frame Recorder", fill="#ECE8EF", font=("Roboto-Bold", int(30.0)))
create_label = canvas.create_text(203.5, 174.5, text="create an", fill="#ECE8EF", font=("Roboto-Bold", int(16.0)))
video_label = canvas.create_text(590.5, 174.5, text="fps video", fill="#ECE8EF", font=("Roboto-Medium", int(16.0)))
switch = tkinter.Scale(from_=100, to=200, orient=tkinter.HORIZONTAL, length=200, activebackground="#C25993"
                       , bg="#C25993", highlightcolor="#C25993", highlightbackground="#C25993", fg="white",
                       troughcolor="white")
#C25993
def edit_checks(clicked):
    if clicked == "mp4":
        if mp4_format.get() == False:
            avi_format.set(True)
        else:
            avi_format.set(False)
    elif clicked == "avi":
        if avi_format.get() == False:
            mp4_format.set(True)
        else:
            mp4_format.set(False)

def result_format():
    if mp4_format.get()==True:
        return ".mp4"
    else:
        return ".avi"

menubar = Menu(root)
video = Menu(menubar, tearoff=0)
about = Menu(menubar, tearoff=0)
video_format = Menu(menubar, tearoff=0)


mp4_format = tkinter.BooleanVar()
mp4_format.set(True)
avi_format = tkinter.BooleanVar()

video_format.add_checkbutton(label=".mp4", onvalue=1, offvalue=0, variable=mp4_format,
                             command=lambda: edit_checks("mp4"))
video_format.add_checkbutton(label=".avi", onvalue=1, offvalue=0, variable=avi_format,
                             command=lambda: edit_checks("avi"))
video.add_cascade(label='Video Format', menu=video_format)

about.add_command(label="Mehmet Mert Altuntas", command=lambda: webbrowser.open("https://github.com/mehmet-mert"))
menubar.add_cascade(label='File', menu=video)
menubar.add_cascade(label="About", menu=about)


# Start button command
def create_vid():
    global out
    screen_size = pyautogui.size()
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    out = cv.VideoWriter("Outputs/FrameRecorder " + find_time() + result_format(), fourcc, switch.get(), (screen_size))


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
        pause["state"] = "disabled"
        start["state"] = "normal"
        canvas.itemconfig(info, text="Paused. Continue Recording with Play")
    elif status == "playing":
        pause["state"] = "normal"
        end["state"] = "normal"
        start["state"] = "disabled"
        canvas.itemconfig(info, text="Recording...")
    elif status == "end":
        canvas.itemconfig(info, text="Video Saved At Outputs Folder. Let's Create Another One!")
        pause["state"] = "disabled"
        end["state"] = "disabled"
        start["state"] = "normal"


start_img = PhotoImage(file=f"assets/start.png")
start = Button(image=start_img, borderwidth=0, highlightthickness=0, command=lambda: start_record(), relief="flat")
pause_img = PhotoImage(file=f"assets/pause.png")
pause = Button(image=pause_img, borderwidth=0, highlightthickness=0, command=lambda: status_playing("stopped"),
               relief="flat")
end_img = PhotoImage(file=f"assets/end.png")
end = Button(image=end_img, borderwidth=0, highlightthickness=0, command=lambda: status_playing("end"), relief="flat")
info = canvas.create_text(400.0, 342.5, text="Start Recording", fill="#ECE8EF", font=("Roboto-Medium", int(16.0)))

# When started
end["state"] = "disabled"
pause["state"] = "disabled"

while True:
    root.update()
    switch.place(x=400, y=176, anchor=tkinter.CENTER)
    start.place(x=318, y=230, width=172, height=58)
    pause.place(x=118, y=230, width=172, height=58)
    end.place(x=518, y=230, width=172, height=58)
    root.config(menu=menubar)
    if status == "playing":
        record()
    elif status == "stopped":
        pass
    elif status == "end":
        out.release()
