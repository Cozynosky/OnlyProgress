from django.shortcuts import render

def face_analysis_view(request):
    return render(request, 'dashboard/face_analysis/face_analysis.html', context={})