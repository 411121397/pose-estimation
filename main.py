import tkinter as tk
import threading
import vlc
import os

# Import your exercise modules
import Arm_Extension_Camera
import ElbowUpDown_Camera
import HorizontalLegRaise_camera
import SingleLeg_camera
import wallWalk_leftHand_Camera
import Ex7_90degreesLegRaise
import calf
import calf_stretch
import Tap_Leg

exercise_status={
    "Ex7_90degreesLegRaise": False,
    "Tap_Leg":False
}

video_path = r"C:\Users\Carl\Desktop\pose-estim\pose-estimation\poseVideos\tutorial.mp4"


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
    def run():
        Ex7_90degreesLegRaise.run_exercise(exercise_status)
        if exercise_status["Ex7_90degreesLegRaise"]:
            update_button_state()
    threading.Thread(target=run).start()

def start_calf():
    threading.Thread(target=calf.run_exercise).start()

def startcalf_stretch():
    threading.Thread(target=calf_stretch.run_exercise).start()

def startTap_Leg():
    def run():
        Tap_Leg.run_exercise(exercise_status)
        if exercise_status["Tap_Leg"]:
            update_button_state()
    threading.Thread(target=run).start()

def update_button_state():
    if exercise_status["Ex7_90degreesLegRaise"]:
        btn_leg_raise["bg"]="gray"
        btn_leg_raise["state"]="disabled"


#SHOW INSTRUCTIONAL VIDEO
import tkinter as tk
import vlc
import os

def show_instructional_video(window, exercise_name):
    def play_video(video_path):
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return

        # VLC Instance
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(video_path)
        player.set_media(media)

        # Embed the video in the Tkinter Canvas
        player.set_hwnd(video_canvas.winfo_id())

        # Play the video
        player.play()

        # Wait until the video finishes
        def check_playback():
            if player.get_state() == vlc.State.Ended:
                start_button["state"] = "normal"  # Enable Start button
            else:
                window.after(100, check_playback)

        check_playback()

    # Clear the current window
    for widget in window.winfo_children():
        widget.destroy()

    # Instruction Label
    video_label = tk.Label(window, text="Watch the instructional video", font=("Arial", 16), bg="#C5EBE8", fg="#008878")
    video_label.pack(pady=10)

    # Video Canvas
    video_canvas = tk.Canvas(window, width=640, height=360, bg="black")
    video_canvas.pack(pady=10)

    # Start Button (disabled initially)
    start_button = tk.Button(
        window,
        text="Start Exercise",
        command=exercise_name,
        font=("Arial", 14),
        bg="#008878",
        fg="white",
        state="disabled"
    )
    start_button.pack(pady=10)

    # Back Button
    btn_back = tk.Button(
        window,
        text="Back",
        command=lambda: open_injury_page(window, "Knee Injuries"),
        font=("Arial", 14),
        bg="#008878",
        fg="white"
    )
    btn_back.pack(pady=10)

    # Play Video
    play_video(video_path)


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

    global btn_leg_raise

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
            #("Single Leg", start_SingleLeg_camera),
            ("Contraction of the thigh/calf", lambda: show_instructional_video(window, start_ex7_90degreesLegRaise)),
            ("Calf Stretch", start_calf),
            ("Step Reaction Training", lambda: show_instructional_video(window, startTap_Leg)),
        ]

    # Add buttons for exercises
    for text, command in exercises:
        bg_color = "gray" if text == "Contraction of the thigh/calf" and exercise_status["Ex7_90degreesLegRaise"] else "#008878"
        state = "disabled" if text == "Contraction of the thigh/calf" and exercise_status["Ex7_90degreesLegRaise"] else "normal"
        btn = tk.Button(
            window,
            text=text,
            command=command,
            font=("Arial", 14),
            bg="#008878",
            fg="white",
            width=22,
            state=state
        )
        btn.pack(pady=10)

        if text == "Contraction of the thigh/calf":
            btn_leg_raise = btn

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
    root.geometry("1920x1080")

    # Set the background color
    root.configure(bg="#C5EBE8")

    # Show the main page
    show_main_page(root)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
