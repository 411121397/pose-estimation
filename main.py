# main.py
import tkinter as tk
from multiprocessing import Process
import threading

# Import your exercise modules
import Arm_Extension_Camera
import Arm_Extension_video
import ElbowUpDown_Camera
import ElbowUpDown_Video
import HorizontalLegRaise_camera
import HorizontalLegRaise
import SingleLeg_camera
import SingleLeg_video
import wallWalk_leftHand_Camera
import wallWalk_LeftHand_video

def start_Arm_Extension_Camera():
    threading.Thread(target=Arm_Extension_Camera.run_exercise).start()

def start_ElbowUpDown_Camera():
    threading.Thread(target=ElbowUpDown_Camera.run_exercise).start()

def start_HorizontalLegRaise_camera():
    threading.Thread(target=HorizontalLegRaise_camera.run_exercise).start()

def start_SingleLeg_camera():
    threading.Thread(target=SingleLeg_camera.run_exercise).start()

def start_wallWalk_leftHand_Camera():
    threading.Thread(target=wallWalk_leftHand_Camera.run_exercise).start()





def main():
    root = tk.Tk()
    root.title("Pose Detection Exercises")

    # Set window size
    root.geometry('700x500')

    # Create buttons for each exercise
    btn_elbow_up_down = tk.Button(root, text="Elbow Up Down", command=start_ElbowUpDown_Camera)
    btn_elbow_up_down.pack(pady=20)

    btn_arm_extension = tk.Button(root, text="Arm Extension", command=start_Arm_Extension_Camera)
    btn_arm_extension.pack(pady=20)

    btn_horizontal_leg_raise = tk.Button(root, text="Horizontal Leg Raise", command=start_HorizontalLegRaise_camera)
    btn_horizontal_leg_raise.pack(pady=20)

    btn_wall_walk = tk.Button(root, text="Wall Walk Left Hand", command=start_wallWalk_leftHand_Camera)
    btn_wall_walk.pack(pady=20)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
