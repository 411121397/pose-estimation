import numpy as np
import os
from pygame import mixer
import cv2
import time
import tkinter as tk

mixer.init()
success_path = os.path.join("sounds", "success.wav")
success_sound = mixer.Sound(success_path)
countdown_path = os.path.join("sounds", "countdown.wav")
countdown_sound = mixer.Sound(countdown_path)
lower_path = os.path.join("sounds", "loweryourleg.wav")
lower_sound = mixer.Sound(lower_path)
upper_path = os.path.join("sounds", "goupper.wav")
upper_sound = mixer.Sound(upper_path)
golower_path = os.path.join("sounds", "golower.wav")
golower_sound = mixer.Sound(golower_path)
visible_path = os.path.join("sounds", "visible.wav")
visible_sound = mixer.Sound(visible_path)
great_path = os.path.join("sounds", "great.wav")
great_sound = mixer.Sound(great_path)
timer_duration = 6
is_timer_active = False
timer_remaining = timer_duration
stop_exercise = False

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points a, b, and c.
    """
    a = np.array(a)  # First point
    b = np.array(b)  # Midpointf
    c = np.array(c)  # Endpoint

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    # Normalize the angle within [0, 180]
    if angle > 180.0:
        angle = 360 - angle

    return angle

def stop_exercise_callback():

    stop_exercise = True

    # Create Tkinter window for "Done" button
def create_tkinter_window():
    root = tk.Tk()
    root.title("Control Panel")
    root.geometry("300x100")
    root.configure(bg="#C5EBE8")

    label = tk.Label(
        root,
        text="Leg Raise Exercise",
        font=("Arial", 14),
        bg="#C5EBE8",
        fg="#008878"
    )
    label.pack(pady=10)

    btn_done = tk.Button(
        root,
        text="Done",
        command=lambda: [stop_exercise_callback(), root.destroy()],
        font=("Arial", 14),
        bg="#FF6347",
        fg="white",
        width=10
    )
    btn_done.pack(pady=10)

    root.mainloop()

def display_countdown(image, seconds_remaining):
        
        overlay = image.copy()
        alpha = 0.6  # Transparency factor

        # Create a semi-transparent rectangle for the countdown text
        cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        # Display the countdown number in the center of the screen
        cv2.putText(
            image,
            str(seconds_remaining),
            (image.shape[1] // 2 - 50, image.shape[0] // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            12,  # Font size
            (255, 255, 255),
            16,
            cv2.LINE_AA
        )

def show_boxes():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    overlay = image.copy()
    feedback_box_height = 80
    cv2.rectangle(overlay, (0, 0), (1280, feedback_box_height), (232, 235, 197), -1)
    counter_box_height = 120
    counter_box_width = 250
    cv2.rectangle(overlay, (0, 720 - counter_box_height), (counter_box_width, 720), (232, 235, 197), -1)
    cv2.rectangle(overlay, (1280 - counter_box_width, 720 - counter_box_height), (1280, 720 ), (232, 235, 197), -1)

    # Blend overlay with the original image to make boxes transparent
    alpha = 0.5  # Transparency factor
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

