import cv2
import mediapipe as mp
import numpy as np
import time
import math


BodyPart = {
    "NOSE": 0,
    "LEFT_EYE_INNER": 1,
    "LEFT_EYE": 2,
    "LEFT_EYE_OUTER": 3,
    "RIGHT_EYE_INNER": 4,
    "RIGHT_EYE": 5,
    "RIGHT_EYE_OUTER": 6,
    "LEFT_EAR": 7,
    "RIGHT_EAR": 8,
    "MOUTH_RIGHT": 10,
    "LEFT_SHOULDER": 11,
    "RIGHT_SHOULDER": 12,
    "LEFT_ELBOW": 13,
    "RIGHT_ELBOW": 14,
    "LEFT_WRIST": 15,
    "RIGHT_WRIST": 16,
    "LEFT_PINKY": 17,
    "RIGHT_PINKY": 18,
    "LEFT_INDEX": 19,
    "RIGHT_INDEX": 20,
    "LEFT_THUMB": 21,
    "RIGHT_THUMB": 22,
    "LEFT_HIP": 23,
    "RIGHT_HIP": 24,
    "LEFT_KNEE": 25,
    "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27,
    "RIGHT_ANKLE": 28,
    "LEFT_HEEL": 29,
    "RIGHT_HEEL": 30,
    "LEFT_FOOT_INDEX": 31,
    "RIGHT_FOOT_INDEX": 32,
}


class PoseDetector:
    def __init__(
        self,
        reps_to_do,
        mode=False,
        compl=1,
        smoothLm=True,
        smoothSg=True,
        seg=False,
        detectionCon=0.5,
        trackCon=0.5,
    ):
        self.mode = mode
        self.compl = compl
        self.smoothLm = smoothLm
        self.smoothSg = smoothSg
        self.seg = seg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.compl,
            smooth_landmarks=self.smoothLm,
            smooth_segmentation=self.smoothSg,
            enable_segmentation=self.seg,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )

        self.finished = False
        self.reps_to_do = reps_to_do
        self.reps = 0
        self.dir = 0

    def find_body_pose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(
                img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
            )

        return img

    def find_landmarks(self, img, draw=True):
        self.landmarks = {}
        if self.results.pose_landmarks:
            for index, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmarks[index] = [cx, cy]
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.landmarks

    def find_angle(self, img, bodypart1, bodypart2, bodypart3, draw=True):
        ax, ay = self.landmarks[bodypart1]
        bx, by = self.landmarks[bodypart2]
        cx, cy = self.landmarks[bodypart3]

        x1x2s = math.pow((ax - bx), 2)
        x1x3s = math.pow((ax - cx), 2)
        x2x3s = math.pow((bx - cx), 2)

        y1y2s = math.pow((ay - by), 2)
        y1y3s = math.pow((ay - cy), 2)
        y2y3s = math.pow((by - cy), 2)

        # angle formula
        # https://muthu.co/using-the-law-of-cosines-and-vector-dot-product-formula-to-find-the-angle-between-three-points/

        cosine_angle = np.arccos(
            (x1x2s + y1y2s + x2x3s + y2y3s - x1x3s - y1y3s)
            / (2 * math.sqrt(x1x2s + y1y2s) * math.sqrt(x2x3s + y2y3s))
        )

        angle = np.degrees(cosine_angle)

        if draw:
            cv2.line(img, (ax, ay), (bx, by), (255, 255, 255), 3)
            cv2.line(img, (cx, cy), (bx, by), (255, 255, 255), 3)
            cv2.circle(img, (ax, ay), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (ax, ay), 15, (0, 0, 255), 2)
            cv2.circle(img, (bx, by), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (bx, by), 15, (0, 0, 255), 2)
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), 2)
            cv2.putText(
                img,
                str(int(angle)),
                (bx - 50, by + 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 255),
                2,
            )

        return angle

    def check_exercise_progress(
        self, img, bodypart1, bodypart2, bodypart3, startang, endang, draw=True
    ):
        if self.reps >= self.reps_to_do:
            self.finished = True
        
        if self.finished:
            img[:] = tuple(reversed((25, 135, 84)))
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "COMPLETED"
            
            textsize = cv2.getTextSize(text, font, 1, 2)[0]
            
            textX = int((img.shape[1] - textsize[0]) / 2)
            textY = int((img.shape[0] + textsize[1]) / 2)
            
            cv2.putText(img, text, (textX, textY), font, 1, (255, 255, 255), 2)

            
        else:
            self.find_body_pose(img, False)
            self.find_landmarks(img, False)

            if len(self.landmarks) != 0:
                angle = self.find_angle(img, bodypart1, bodypart2, bodypart3)

                if startang > endang:
                    per = 100 - int(np.interp(angle, (endang, startang), (0, 100)))

                else:
                    per = 100 - int(np.interp(angle, (startang, endang), (0, 100)))

                if per == 100 and self.dir == 0:
                    self.reps += 0.5
                    self.dir = 1
                elif per == 0 and self.dir == 1:
                    self.reps += 0.5
                    self.dir = 0
                
                if self.dir == 0 :
                    start_angle = 0
                    end_angle = (360/100*per)
                
                elif self.dir == 1:
                    start_angle = 360
                    end_angle = (360/100*(100-per))
                    
                cv2.ellipse(img, (55, 55), (50,50), 0, start_angle, end_angle, (255,0,0), -1)
                cv2.circle(img, (55,55), 40, (0,255,0), -1)
                
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = str(self.reps_to_do - int(self.reps))
            
                textsize = cv2.getTextSize(text, font, 0.5, 2)[0]
            
                textX = int((100 - textsize[0]) / 2)
                textY = int((115 + textsize[1]) / 2)
            
                cv2.putText(img, text, (textX, textY), font, 1, (0, 0, 255), 2)
                    
        
def live_demo():
    cap = cv2.VideoCapture(0)
    detector = PoseDetector(reps_to_do=5)

    while True:
        succ, frame = cap.read()
        detector.check_exercise_progress(
            frame,
            BodyPart["RIGHT_SHOULDER"],
            BodyPart["RIGHT_ELBOW"],
            BodyPart["RIGHT_WRIST"],
            160,
            50,
        )

        cv2.imshow("image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

def check_pose_demo(path):
    detector = PoseDetector(reps_to_do=5)
    cap = cv2.VideoCapture(path)
    
    # Read until video is completed
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == True:
        
            # Display the resulting frame
            detector.check_exercise_progress( frame,
            BodyPart["RIGHT_SHOULDER"],
            BodyPart["RIGHT_ELBOW"],
            BodyPart["RIGHT_WRIST"],
            160,
            50,)
            cv2.imshow('Frame',frame)
        
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        # Break the loop
        else: 
            break
    
    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    check_pose_demo("D:/Projects/Magisterka/OnlyProgress/static/data/downloaded/test_video/videoplayback.mp4")
    #live_demo()
