import cv2
import mediapipe as mp
import numpy as np
import time
import threading
from Common import *



def run_exercise(status_dict):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv2.namedWindow('Leg Raise Exercise', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Leg Raise Exercise', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    reps = 0
    stage = 'down'
    warning_message = None
    last_lower_sound_time=None
    timer_remaining = None 

    # Start the Tkinter window in a separate thread
    threading.Thread(target=create_tkinter_window, daemon=True).start()

   

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

            # Draw pose landmarks on the image
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
            current_timer = timer_remaining if timer_remaining is not None else 0
            image = create_feedback_overlay(image, counter=current_timer, reps=reps)
            cv2.imshow('Leg Raise Exercise', image)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    status_dict["Ex7_90degreesLegRaise"] = True


if __name__ == "__main__":
    status_dict = {"Ex7_90degreesLegRaise": False}
    run_exercise(status_dict)
