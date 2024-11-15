import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe pose and drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Path to your video file
video_path = "poseVideos/11.mp4"  # Replace this with the path to your video

# Set up video feed
cap = cv2.VideoCapture(video_path)

# Counter variables for side leg raises
counter = 0
stage = None
frame_skip = 2  # Skipping frames to make video play faster
frame_count = 0

# Setup Mediapipe Pose with specified confidence levels
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frames for faster video processing
        if frame_count % frame_skip != 0:
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # Print coordinates for debugging
            print("Hip:", hip, "Ankle:", ankle)

            # Detect side leg raise based on horizontal position of ankle relative to hip
            # Adjust these thresholds based on the printed values
            if ankle[0] > hip[0] + 0.1:  # Leg raised to the side, adjust threshold as needed
                stage = "up"
            elif ankle[0] <= hip[0] + 0.05:  # Leg returns down, adjust threshold as needed
                if stage == "up":
                    stage = "down"
                    counter += 1  # Count one repetition

        except Exception as e:
            print("Error:", e)
            pass

        # Render the counter and stage text on the image
        cv2.rectangle(image, (0, 0), (225, 73), (255, 0, 0), -1)  # Blue box background (BGR: 255, 0, 0)
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'Stage', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage if stage else "None",
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Draw pose landmarks on the image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        # Display the output
        cv2.imshow('Mediapipe Feed', image)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
