import cv2
import mediapipe as mp
import numpy as np
import time
import os
from pygame import mixer
import tkinter as tk
import threading


def calculate_angle(a, b, c):
    """
    Calculate the angle between three points a, b, and c.
    """
    a = np.array(a)  # First point
    b = np.array(b)  # Midpoint
    c = np.array(c)  # Endpoint

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    # Normalize the angle within [0, 180]
    if angle > 180.0:
        angle = 360 - angle

    return angle

def run_exercise(status_dict):
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    reps = 0
    stage = 'down'  
    timer_duration = 6  
    is_timer_active = False
    timer_remaining = timer_duration
    warning_message = None 
    stop_exercise=False

    def stop_exercise_callback():
        nonlocal stop_exercise
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

    # Start the Tkinter window in a separate thread
    threading.Thread(target=create_tkinter_window, daemon=True).start()



    mixer.init()
    success_path = os.path.join("sounds", "success.wav")
    success_sound = mixer.Sound(success_path)
    countdown_path=os.path.join("sounds", "countdown.wav")
    countdown_sound=mixer.Sound(countdown_path)
    lower_path = os.path.join("sounds", "loweryourleg.wav")
    lower_sound = mixer.Sound(lower_path)
    last_lower_sound_time = None  
    upper_path=os.path.join("sounds", "goupper.wav")
    upper_sound=mixer.Sound(upper_path)
    golower_path=os.path.join("sounds", "golower.wav")
    golower_sound=mixer.Sound(golower_path)
    visible_path=os.path.join("sounds", "visible.wav")
    visible_sound=mixer.Sound(visible_path)
    great_path=os.path.join("sounds", "great.wav")
    great_sound=mixer.Sound(great_path)


    countdown_complete = False

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
        

    # Perform the countdown
    start_time = time.time()
    countdown_sound.play()
    while time.time() - start_time < timer_duration:
        ret, frame = cap.read()
        if not ret:
            break

        seconds_remaining = int(timer_duration - (time.time() - start_time))
        display_countdown(frame, seconds_remaining)
        cv2.imshow("Leg Raise Exercise", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

    # Set flag after countdown
    countdown_complete = True



    # Setup Mediapipe Pose with specified confidence levels
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            
            if stop_exercise:  # Check if "Done" button was pressed
                status_dict["Ex7_90degreesLegRaise"] = True
                break


            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB and make it non-writable to improve performance
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            warning_message = None  # Reset warning message for each frame

            # Extract pose landmarks
            try:
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    # Check if required landmarks are detected
                    required_landmarks = {
                        'Left Hip': mp_pose.PoseLandmark.LEFT_HIP.value,
                        'Left Knee': mp_pose.PoseLandmark.LEFT_KNEE.value,
                        'Left Ankle': mp_pose.PoseLandmark.LEFT_ANKLE.value
                    }
                    missing_landmarks = []
                    for name, idx in required_landmarks.items():
                        visibility = landmarks[idx].visibility
                        if visibility < 0.5 or np.isnan(landmarks[idx].x) or np.isnan(landmarks[idx].y):
                            missing_landmarks.append(name)

                    if missing_landmarks:
                        warning_message = f"Adjust Position: {', '.join(missing_landmarks)} not detected!"

                    else:
                        # Get coordinates for hip, knee, and ankle
                        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        # Calculate the angle between hip, knee, and ankle
                        angle = calculate_angle(hip, knee, ankle)

                        # Visualize the angle 
                        cv2.putText(image, str(int(angle)),
                                    tuple(np.multiply(knee, [640, 480]).astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                        # Exercise logic with state machine
                        if angle > 97:
                            warning_message = "Leg is too down. Raise your leg."
                            current_time = time.time()
                            if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                                    upper_sound.play()
                                    last_lower_sound_time = current_time
                            if stage == 'hold' or stage == 'up':
                                # Leg has been lowered, reset for next rep
                                stage = 'down'
                                is_timer_active = False
                                timer_remaining = timer_duration
                                last_lower_sound_time = None  # Reset lower sound timer
                        elif angle < 85:
                            warning_message = "Leg is too up. Lower your leg."
                            current_time = time.time()
                            if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                                    golower_sound.play()
                                    last_lower_sound_time = current_time
                        else:

                            # Angle is between 85 and 97 degrees
                            if stage == 'down':
                                # Start timer
                                timer_start = time.time()
                                is_timer_active = True
                                stage = 'up'
                                current_time = time.time()
                                if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                                        great_sound.play()
                                        last_lower_sound_time = current_time
                            elif stage == 'up':
                                # Continue timing
                                elapsed_time = time.time() - timer_start
                                timer_remaining = timer_duration - elapsed_time
                                if timer_remaining <= 0:
                                    # Rep completed
                                    success_sound.play()
                                    warning_message = "Great! Hold Completed!"
                                    reps += 1
                                    is_timer_active = False
                                    timer_remaining = timer_duration
                                    stage = 'hold'  # Waiting for leg to be lowered
                                    last_lower_sound_time = None  # Reset lower sound timer
                                    current_time = time.time()
                                    if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                                        lower_sound.play()
                                        last_lower_sound_time = current_time
                            elif stage == 'hold':
                                warning_message = "Lower your leg"
                                

                else:
                    warning_message = "Pose not detected. Make sure full body is visible."
                    current_time = time.time()
                    if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                        visible_sound.play()
                        last_lower_sound_time = current_time
            except Exception as e:
                warning_message = "Pose not detected. Make sure full body is visible."
                print("Error:", e)
                current_time = time.time()
                if last_lower_sound_time is None or (current_time - last_lower_sound_time) >= 5:
                    visible_sound.play()
                    last_lower_sound_time = current_time

            # Overlay for feedback
            overlay = image.copy()
            feedback_box_height = 60
            cv2.rectangle(overlay, (0, 0), (640, feedback_box_height), (232, 235, 197), -1)
            counter_box_height = 60
            counter_box_width = 180
            cv2.rectangle(overlay, (0, 480 - counter_box_height), (counter_box_width, 480), (232, 235, 197), -1)
            cv2.rectangle(overlay, (640 - counter_box_width, 480 - counter_box_height), (640, 480), (232, 235, 197), -1)

            # Blend overlay with the original image to make boxes transparent
            alpha = 0.5  # Transparency factor
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            # Display warning message
            if warning_message:
                if warning_message == "Good Job! Keep Going":
                    cv2.putText(image, warning_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(image, warning_message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            # Display timer if active
            if is_timer_active:
                cv2.putText(image, str(int(timer_remaining)), (20, 480 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            # Render repetition counter
            cv2.putText(image, 'REPS', (640 - counter_box_width + 10, 480 - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(reps), (640 - counter_box_width + 8, 480 - 10),  # Show the counter
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

            # Draw pose landmarks on the image
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            cv2.imshow('Leg Raise Exercise', image)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    status_dict["Ex7_90degreesLegRaise"]= True

if __name__ == "__main__":
    status_dict={"Ex7_90degreesLegRaise": False}
    run_exercise(status_dict)
