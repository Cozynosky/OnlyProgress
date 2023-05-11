import cv2


from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render

from .predictors import predict_bmi

class VideoCamera(object):
    
    def __init__(self) -> None:
        self.video = cv2.VideoCapture(0)
        
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image = predict_bmi(image)
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

        
def face_analysis_view(request):
    return render(request, 'dashboard/face_analysis/face_analysis.html', context={})