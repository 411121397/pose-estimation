import cv2
import mediapipe as mp
import numpy as np

<<<<<<< HEAD

def run_exercise():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    video_path = "poseVideos/11.mp4"

    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None

=======
def run_exercise():
        
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose


    video_path = "poseVideos/11.mp4"  


    cap = cv2.VideoCapture(0)


    counter = 0
    stage = None


>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
    # Setup Mediapipe Pose with specified confidence levels
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

<<<<<<< HEAD
=======
            

>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
<<<<<<< HEAD
                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # print("Hip:", hip, "Ankle:", ankle)

=======
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                
                #print("Hip:", hip, "Ankle:", ankle)

                
>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
                if ankle[0] > hip[0] + 0.1:  # Leg raised to the side
                    stage = "up"
                elif ankle[0] <= hip[0] + 0.05:  # Leg returns down
                    if stage == "up":
                        stage = "down"
<<<<<<< HEAD
                        counter += 1
=======
                        counter += 1 
>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24

            except Exception as e:
                print("Error:", e)
                pass

<<<<<<< HEAD
=======
            
>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
            cv2.rectangle(image, (0, 0), (225, 73), (255, 0, 0), -1)
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

<<<<<<< HEAD
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            cv2.imshow('Horizontal Leg Raise', image)

=======
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

        
            cv2.imshow('Horizontal Leg Raise', image)

            
>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

<<<<<<< HEAD

if __name__ == "__main__":
    run_exercise()
=======
if __name__ == "__main__":
    run_exercise()
>>>>>>> 5379c78257fcfaaba7bce192b22ec2ff9b37cd24
