import math
from tkinter import *
from PIL import Image, ImageTk
import pygame.mixer

# ---------------------------- CONSTANTS ------------------------------- #
DEFAULT = "#f7f5dd"
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#faee5a"
BLUE = "#7b9acc"
FONT = ("Courier", 35, "bold")
FONT_BTN = ("Courier", 12, "bold")
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
WORK_MIN = 60

# Variables
timer_running = False
timer = None
reps = 0
after_id = ""

pygame.mixer.init()


def play_sound(music):
    sound = pygame.mixer.Sound(music)
    sound.play()


def stop_sound():
    pygame.mixer.stop()


def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)


def reset_timer():
    global reps, timer_running, after_id
    if after_id:
        window.after_cancel(after_id)
    canvas.itemconfig(text_timer, text="00:00")
    my_label.config(text="TIMER", fg=GREEN)
    check_marks.config(text="")
    reps = 0
    timer_running = False
    after_id = ""
    stop_sound()

    canvas.itemconfig(image_id, image=work_image)
    window.config(bg=DEFAULT)
    canvas.config(bg=DEFAULT)
    my_label.config(bg=DEFAULT)


def start_timer():
    global timer_running, timer, reps
    if not timer_running:
        timer_running = True
        reps += 1

        if reps % 6 == 0:  # Long break
            count_down(LONG_BREAK_MIN * 60)
            my_label.config(text="Activity", fg=RED)
            play_sound("break.WAV")
            focus_window("on")
            canvas.itemconfig(image_id, image=long_break_image)
            window.config(bg=YELLOW)
            canvas.config(bg=YELLOW)
            my_label.config(bg=YELLOW)
            check_marks.config(bg=YELLOW)
        elif reps % 2 == 0:  # Short break
            count_down(SHORT_BREAK_MIN * 60)
            my_label.config(text="Play Time", fg=PINK)
            play_sound("break.WAV")
            focus_window("on")
            canvas.itemconfig(image_id, image=short_break_image)
            window.config(bg=BLUE)
            canvas.config(bg=BLUE)
            my_label.config(bg=BLUE)
            check_marks.config(bg=BLUE)
        else:
            count_down(WORK_MIN * 60)
            my_label.config(text="WORK", fg=RED)
            play_sound("start-work.WAV")
            focus_window("off")
            canvas.itemconfig(image_id, image=work_image)
            window.config(bg=DEFAULT)
            canvas.config(bg=DEFAULT)
            my_label.config(bg=DEFAULT)
            check_marks.config(bg=DEFAULT)


def count_down(count):
    global timer_running, timer, after_id
    mins, secs = divmod(count, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    canvas.itemconfig(text_timer, text=timer)
    if count > 0 and timer_running:
        after_id = window.after(1000, count_down, count - 1)
    else:
        if timer_running:
            timer_running = False
            start_timer()
            marks = ""
            work_sessions = math.floor(reps / 2)
            for _ in range(work_sessions):
                marks += "✔"
            check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.update_idletasks()
window.title("TotTime Manager")
window.config(padx=40, pady=50, bg=DEFAULT)

# Load and resize images for different states
work_img = Image.open("apple.png").resize((380, 380), Image.Resampling.LANCZOS)
short_break_img = Image.open("toys.png").resize((300, 350), Image.Resampling.LANCZOS)
long_break_img = Image.open("activity.png").resize((280, 350), Image.Resampling.LANCZOS)

work_image = ImageTk.PhotoImage(work_img)
short_break_image = ImageTk.PhotoImage(short_break_img)
long_break_image = ImageTk.PhotoImage(long_break_img)

# Create canvas and display resized image
canvas = Canvas(width=380, height=380, bg=DEFAULT, highlightthickness=0)
image_id = canvas.create_image(190, 190, image=work_image)
text_timer = canvas.create_text(190, 220, text="00:00", fill="white", font=FONT)
canvas.grid(column=2, row=2)

my_label = Label(text="TIMER", font=FONT, bg=DEFAULT, fg=GREEN, highlightthickness=0)
my_label.grid(column=2, row=1)

check_marks = Label(font=FONT, bg=DEFAULT, fg=GREEN)
check_marks.grid(column=2, row=4)

# Buttons
start_button = Button(text="Start",
                      command=start_timer,
                      highlightthickness=0,
                      bg="#4CAF50",
                      fg="white",
                      font=FONT_BTN,
                      relief="raised",
                      padx=10, pady=5)
start_button.grid(column=1, row=3)

reset_button = Button(text="Reset",
                      command=reset_timer,
                      highlightthickness=0,
                      bg="#f44336",
                      fg="white",
                      font=FONT_BTN,
                      relief="raised",
                      padx=10, pady=5)
reset_button.grid(column=3, row=3)

window.mainloop()
