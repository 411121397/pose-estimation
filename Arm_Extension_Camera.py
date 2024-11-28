import cv2
import mediapipe as mp
import numpy as np


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


def run_exercise():
    # Initialize mediapipe pose and drawing utilities
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None
    feedback = ""

    # Setup Mediapipe Pose with specified confidence levels
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                leftwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # angle between shoulder, elbow, and wrist
                angle = calculate_angle(leftwrist, shoulder, wrist)
                cv2.putText(image, str(int(angle)),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Define the stages based on angle
                feedback_color = (0, 255, 0)
                if angle > 177:
                    stage = "start"
                    feedback = "Good form! Keep it up!"
                elif angle < 70 and stage == "start":
                    stage = "half-circle"
                    counter += 1
                    feedback = "Good job! Keep going!"

                # Provide feedback if the angle is too large or small
                elif angle < 40:
                    feedback = "Bad form! Try to extend your arm more!"
                elif angle > 160:
                    feedback = "Bad form! Try to bend your elbow more!"
                else:
                    feedback = "Your arm needs to be visible"

            except Exception as e:
                print("Error:", e)
                pass

            # Set feedback color
            feedback_color = (0, 0, 255)  # Default to red
            if feedback == "Good form! Keep it up!":
                feedback_color = (0, 255, 0)  # Green

            # Display feedback with the corresponding color
            cv2.putText(image, feedback, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, feedback_color, 2, cv2.LINE_AA)

            # Stage box (blue background) at the top-left corner
            stage_box_height = 60
            stage_box_width = 160

            # Create a blue box for the counter at the bottom-right corner
            counter_box_height = 60
            counter_box_width = 160
            cv2.rectangle(image, (640 - counter_box_width - 10, 480 - counter_box_height - 10),
                          (640 - 10, 480 - 10), (255, 0, 0), -1)  # Blue background for the counter

            cv2.putText(image, 'REPS', (640 - counter_box_width + 10, 480 - counter_box_height + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

            # Show the counter
            cv2.putText(image, str(counter), (640 - counter_box_width + 10, 480 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage box (blue background) at the bottom-left corner
            cv2.rectangle(image, (10, 480 - stage_box_height - 10), (10 + stage_box_width, 480 - 10),
                          (255, 0, 0), -1)  # Blue background for the stage info at the bottom-left

            # Display stage label and info at the bottom-left corner
            cv2.putText(image, 'Stage', (20, 480 - stage_box_height + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, stage if stage else "None", (20, 480 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            cv2.imshow('Arm Extension', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_exercise()
