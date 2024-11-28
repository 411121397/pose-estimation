import tkinter as tk
import threading

# Import your exercise modules
import Arm_Extension_Camera
import ElbowUpDown_Camera
import HorizontalLegRaise_camera
import SingleLeg_camera
import wallWalk_leftHand_Camera
import Ex7_90degreesLegRaise
# Define a function to start exercises
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

def start_ex7_90degreesLegRaise():
    threading.Thread(target=Ex7_90degreesLegRaise.run_exercise).start()

# Function to clear the current window and show the main page again
def show_main_page(window):
    for widget in window.winfo_children():
        widget.destroy()

    # Add the title label
    title_label = tk.Label(
        window,
        text="My Pocket Physio",
        font=("Arial", 20, "bold"),
        bg="#C5EBE8",
        fg="#008878"
    )
    title_label.pack(pady=(30, 10))

    # Add a body of text
    body_text = tk.Label(
        window,
        text="Welcome to My Pocket Physio, the solution to all your body aches and injuries.",
        font=("Arial", 16),
        bg="#C5EBE8",
        fg="#008878",
        wraplength=700,
        justify="center"
    )
    body_text.pack(pady=(10, 30))

    # Add text for instructions
    instruction_text = tk.Label(
        window,
        text="Please select your injury type:",
        font=("Arial", 14),
        bg="#C5EBE8",
        fg="#008878"
    )
    instruction_text.pack(pady=20)

    # Add buttons for injury types
    btn_arm_injury = tk.Button(
        window,
        text="Arm Injury",
        command=lambda: open_injury_page(window, "Arm Injuries"),
        font=("Arial", 16),
        width=20,
        bg="#008878",
        fg="white"
    )
    btn_arm_injury.pack(pady=20)

    btn_knee_injury = tk.Button(
        window,
        text="Knee Injury",
        command=lambda: open_injury_page(window, "Knee Injuries"),
        font=("Arial", 16),
        width=20,
        bg="#008878",
        fg="white"
    )
    btn_knee_injury.pack(pady=20)

# Function to show injury pages (both arm and knee)
def open_injury_page(window, injury_type):
    # Clear the current window content
    for widget in window.winfo_children():
        widget.destroy()

    # Add the title for the injury page
    title_label = tk.Label(
        window,
        text=injury_type,
        font=("Arial", 18, "bold"),
        bg="#C5EBE8",
        fg="#008878"
    )
    title_label.pack(pady=20)

    # Based on the injury type, show the corresponding exercises
    if injury_type == "Arm Injuries":
        exercises = [
            ("Elbow Up Down", start_ElbowUpDown_Camera),
            ("Arm Extension", start_Arm_Extension_Camera),
            ("Wall Walk Left Hand", start_wallWalk_leftHand_Camera)
        ]
    else:
        exercises = [
            ("Horizontal Leg Raise", start_HorizontalLegRaise_camera),
            ("Single Leg", start_SingleLeg_camera),
            ("Contraction of the thigh/calf", start_ex7_90degreesLegRaise)
        ]

    # Add buttons for exercises
    for text, command in exercises:
        btn = tk.Button(
            window,
            text=text,
            command=command,
            font=("Arial", 14),
            bg="#008878",
            fg="white",
            width=22
        )
        btn.pack(pady=10)

    # Add a "Back" button to return to the main page
    btn_back = tk.Button(
        window,
        text="Back",
        command=lambda: show_main_page(window),
        font=("Arial", 14),
        bg="#008878",
        fg="white"
    )
    btn_back.pack(pady=20, anchor="w", padx=20)

# Main Window
def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Pose Detection Main Menu")
    root.geometry("800x600")

    # Set the background color
    root.configure(bg="#C5EBE8")

    # Show the main page
    show_main_page(root)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
