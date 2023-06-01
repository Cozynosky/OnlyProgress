import cv2

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now

from .models import Exercise, Workout
from .pose import PoseDetector, BodyPart
from .forms import WorkoutForm

class VideoCamera(object):
    
    def __init__(self, bodypart_a, bodypart_b, bodypart_c, start_angle, end_angle, reps) -> None:
        self.video = cv2.VideoCapture(0)
        self.pose_detector = PoseDetector()
        self.bodypart_a = bodypart_a
        self.bodypart_b = bodypart_b
        self.bodypart_c = bodypart_c
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.reps = reps
        
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        self.pose_detector.check_exercise_progress(image, self.bodypart_a, self.bodypart_b, self.bodypart_c, self.start_angle, self.end_angle)
        
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
def camera_feed(request, exercise_id, reps):
    exercise = Exercise.objects.get(pk=exercise_id)
    return StreamingHttpResponse(gen_camera(VideoCamera(exercise.bodypart_a, exercise.bodypart_b, exercise.bodypart_c, exercise.start_angle, exercise.end_angle, reps)),content_type="multipart/x-mixed-replace;boundary=frame")

        
def train_with_ai_view(request, exercise_id, reps):
    exercise = Exercise.objects.get(pk=exercise_id)
    context = {
        'exercise':exercise,
        'reps':reps
    }
    return render(request, 'dashboard/workout/train_with_ai.html', context=context)

def exercises_view(request):
    exercises_list = Exercise.objects.all()
    context = {
        'exercises': exercises_list
    }
    return render(request, 'dashboard/workout/exercises.html', context=context)

def add_training_view(request, exercise_id):
    exercise = Exercise.objects.get(pk=exercise_id)
    if request.method == "POST":
        if 'DONE' in request.POST:
            form = WorkoutForm(request.POST)
            if form.is_valid():
                reps = form.cleaned_data["reps"]
                date = form.cleaned_data["date"]

                if  len(Workout.objects.filter(date=date).filter(exercise=exercise))==0:
                    workout = Workout(
                        profile=request.user.profile,
                        date=date,
                        reps=reps,
                        exercise=exercise
                    )
                    workout.save()
                else:
                    workout = Workout.objects.get(date=date, exercise=exercise)
                    workout.reps = workout.reps + reps
                    workout.sets = workout.sets + 1
                    workout.save()
                    
                return redirect("dashboard:workout:add_training", exercise_id=exercise_id)
            else:
                context = {
                'exercise':exercise,
                'form': form
                }
                return render(request, 'dashboard/workout/add_training.html', context=context)
        else:
            form = WorkoutForm(request.POST)
            if form.is_valid():
                reps = form.cleaned_data["reps"]
                return redirect("dashboard:workout:train_with_ai", exercise_id=exercise_id, reps=reps)
            else:
                context = {
                'exercise':exercise,
                'form': form
                }
                return render(request, 'dashboard/workout/add_training.html', context=context)
    else:
        form = WorkoutForm(initial={"date": now()})
        context = {
            'exercise':exercise,
            'form': form
        }
        return render(request, 'dashboard/workout/add_training.html', context=context)
    
def exercise_history_view(request, exercise_id, page):
    exercise = Exercise.objects.get(id=exercise_id)
    all_workouts = request.user.profile.workout_set.all().filter(exercise_id=exercise_id).order_by("-date")
    paginator = Paginator(all_workouts, 10)
    
    try:
        workouts = paginator.page(page)
    except PageNotAnInteger:
        workouts = paginator.page(1)
    except EmptyPage:
        workouts = paginator.page(paginator.num_pages)
    
    
    reps = []
    dates = []
    
    for workout in reversed(workouts):
        dates.append(workout.date)
        reps.append(workout.reps)
        
    labels = list(map(lambda x: x.strftime("%d/%m/%Y"), dates))
    
    context = {
        'exercise': exercise,
        'workouts':workouts,
        'labels':labels,
        'reps':reps
    }
    return render(request, 'dashboard/workout/exercise_history.html', context=context)