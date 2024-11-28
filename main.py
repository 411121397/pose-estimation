import tkinter as tk
import threading

# Import your exercise modules
import Arm_Extension_Camera
import ElbowUpDown_Camera
import HorizontalLegRaise_camera
import SingleLeg_camera
import wallWalk_leftHand_Camera


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


def open_arm_injuries():
    # Create a new window for Arm Injuries
    arm_window = tk.Toplevel()
    arm_window.title("Arm Injuries")
    arm_window.geometry("500x400")

    # Add buttons for arm injury exercises
    btn_elbow_up_down = tk.Button(arm_window, text="Elbow Up Down", command=start_ElbowUpDown_Camera)
    btn_elbow_up_down.pack(pady=20)

    btn_arm_extension = tk.Button(arm_window, text="Arm Extension", command=start_Arm_Extension_Camera)
    btn_arm_extension.pack(pady=20)

    btn_wall_walk = tk.Button(arm_window, text="Wall Walk Left Hand", command=start_wallWalk_leftHand_Camera)
    btn_wall_walk.pack(pady=20)


def open_knee_injuries():
    # Create a new window for Knee Injuries
    knee_window = tk.Toplevel()
    knee_window.title("Knee Injuries")
    knee_window.geometry("500x400")

    # Add buttons for knee injury exercises
    btn_horizontal_leg_raise = tk.Button(knee_window, text="Horizontal Leg Raise", command=start_HorizontalLegRaise_camera)
    btn_horizontal_leg_raise.pack(pady=20)

    btn_single_leg = tk.Button(knee_window, text="Single Leg", command=start_SingleLeg_camera)
    btn_single_leg.pack(pady=20)


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Pose Detection Main Menu")
    root.geometry("500x400")

    # Add buttons for injury types
    btn_arm_injury = tk.Button(root, text="Arm Injury", command=open_arm_injuries, font=("Arial", 14), width=20)
    btn_arm_injury.pack(pady=50)

    btn_knee_injury = tk.Button(root, text="Knee Injury", command=open_knee_injuries, font=("Arial", 14), width=20)
    btn_knee_injury.pack(pady=50)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
