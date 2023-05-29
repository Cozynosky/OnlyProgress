import cv2

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render

from .pose import PoseDetector, BodyPart

class VideoCamera(object):
    
    def __init__(self) -> None:
        self.video = cv2.VideoCapture(0)
        self.pose_detector = PoseDetector()

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        self.pose_detector.check_exercise_progress(image, BodyPart.RIGHT_SHOULDER.value, BodyPart.RIGHT_ELBOW.value, BodyPart.RIGHT_WRIST.value, 50, 160)
        
        # cv2.putText(img, f'{per} %', (img.shape[1] - 150, img.shape[0] - 150), cv2.FONT_HERSHEY_PLAIN, 4,
        #             (0, 255, 0), 4)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen_camera(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        
@gzip.gzip_page
def camera_feed(request): 
    return StreamingHttpResponse(gen_camera(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")

        
def workout_view(request):
    context = {
        "exercise_name": "Burps"
    }
    return render(request, 'dashboard/workout/workout.html', context=context)