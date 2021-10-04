import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Key, Controller
import webview

def shot(window):   
    keyboard = Controller()
    mp_pose = mp.solutions.pose
    mp_drawing =  mp.solutions.drawing


    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle

    lst = []
    lst = lst[-500:]
    # VIDEO FEED
    cap = cv2.VideoCapture(0)
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=0, enable_segmentation=False, static_image_mode=False) as pose:
        while cap.isOpened():
            _, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Get coordinates
                shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate angle
                angle_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
                angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)
                
                if angle_l > 140 or angle_r > 120 and True not in lst:
                    lst.append(True)
                    shot = True
                #    font = cv2.FONT_HERSHEY_PLAIN
            #       cv2.putText(image, 'Shot!', 
            #                          (10,height-10), font, 4, 
            #                         (0,0,0), 5, cv2.LINE_AA) 
                    #print("shot")
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                else:
                    lst.append(False)
                    shot = False

                    
                
                # Visualize angle
                #cv2.putText(image, str(angle), 
                #               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                #               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #                    )
                        
            except:
                pass
            
            
            # Render detections
            if shot == False:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                         )      
            else:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)     
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                cap.release()
                cv2.destroyAllWindows()


if __name__ == '__main__':
    window = webview.create_window('Cricket!', 'https://doodlecricket.github.io/#/')
    webview.start(shot, window)
    