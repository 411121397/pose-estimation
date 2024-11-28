import cv2
import mediapipe as mp
import numpy as np

def run_exercise():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Open webcam for pose detection
    cap = cv2.VideoCapture(0)

    counter = 0  # Count the number of repetitions
    stage = None  # Track the stage of the exercise

    # Setup Mediapipe Pose with specified confidence levels
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from webcam.")
                break

            # Convert the frame to RGB for Mediapipe processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Optimize for performance
            results = pose.process(image)

            # Convert back to BGR for OpenCV rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                # Extract landmarks
                landmarks = results.pose_landmarks.landmark
                hip = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
                ]
                ankle = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
                ]

                # Check exercise stages based on leg position
                if ankle[0] > hip[0] + 0.1:  # Leg raised to the side
                    stage = "up"
                elif ankle[0] <= hip[0] + 0.05 and stage == "up":  # Leg returns down
                    stage = "down"
                    counter += 1  # Increment counter when leg lowers

            except Exception as e:
                print("Error processing landmarks:", e)
                pass

            # Display counter and stage on the screen
            cv2.rectangle(image, (0, 0), (225, 73), (255, 0, 0), -1)
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage if stage else "None",
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

            # Draw pose landmarks on the frame
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            # Display the frame
            cv2.imshow('Horizontal Leg Raise', image)

            # Break loop on 'q' key press
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_exercise()
