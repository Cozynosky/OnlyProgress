from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from bodyfatpredictor.fatpredictor import predict_bodyfat, calculate_bmi
from .forms import NewBodystatsForm
from .models import BodyStats


def latest_bodystats_view(request):
    pk = request.user.profile.bodystats_set.last().pk

    return redirect("dashboard:bodystats:show_bodystats", id=pk)


def show_bodystats_view(request, id):
    try:
        bodystats_set = BodyStats.objects.get(pk=id)
        #bodystats_set = model_to_dict(bodystats_set)
        
        creation_time = bodystats_set.date.strftime("%d/%m/%Y - %H:%M")
        bmi = {"val": bodystats_set.bmi}
        bodyfat = {"val": bodystats_set.bodyfat}
        
        bodystats = {
            "age": {"val": bodystats_set.age, "unit": "years"},
            "weight": {"val": bodystats_set.weight, "unit": "kg"},
            "height": {"val": bodystats_set.height, "unit": "cm"},
            "neck": {"val": bodystats_set.neck, "unit": "cm"},
            "chest": {"val": bodystats_set.chest, "unit": "cm"},
            "abdomen": {"val": bodystats_set.abdomen, "unit": "cm"},
            "hip": {"val": bodystats_set.hip, "unit": "cm"},
            "thigh": {"val": bodystats_set.thigh, "unit": "cm"},
            "knee": {"val": bodystats_set.knee, "unit": "cm"},
            "ankle": {"val": bodystats_set.ankle, "unit": "cm"},
            "biceps": {"val": bodystats_set.biceps, "unit": "cm"},
            "forearm": {"val": bodystats_set.forearm, "unit": "cm"},
            "wrist": {"val": bodystats_set.wrist, "unit": "cm"}
        }
        
        if len(request.user.profile.bodystats_set.all()) > 1:
            all_bodystats = list(request.user.profile.bodystats_set.all())
            current_bodystats_id = all_bodystats.index(bodystats_set)
            
            print(all_bodystats)
            
            if current_bodystats_id != 0:
                curr = model_to_dict(all_bodystats[current_bodystats_id])
                prev = model_to_dict(all_bodystats[current_bodystats_id-1])
                
                for stat_name in bodystats:
                    if curr[stat_name] > prev[stat_name]:
                        bodystats[stat_name]["change"] = "more"
                    elif curr[stat_name] < prev[stat_name]:
                        bodystats[stat_name]["change"] = "less"
                    else:
                        bodystats[stat_name]["change"] = "same"

        context = {"date": creation_time, "bmi": bmi, "bodyfat": bodyfat, "bodystats": bodystats}

    except BodyStats.DoesNotExist:

        context = None

    return render(request, "dashboard/bodystats/show_bodystats.html", context=context)


def history_bodystats_view(request):
    pass


def add_bodystats_view(request):
    if request.method == "POST":
        form = NewBodystatsForm(request.POST)
        if form.is_valid():
            BodyStats.objects.create(
                profile=request.user.profile,
                date=form.cleaned_data["date"],
                age=form.cleaned_data["age"],
                weight=form.cleaned_data["weight"],
                height=form.cleaned_data["height"],
                neck=form.cleaned_data["neck"],
                chest=form.cleaned_data["chest"],
                abdomen=form.cleaned_data["abdomen"],
                hip=form.cleaned_data["hip"],
                thigh=form.cleaned_data["thigh"],
                knee=form.cleaned_data["knee"],
                ankle=form.cleaned_data["ankle"],
                biceps=form.cleaned_data["biceps"],
                forearm=form.cleaned_data["forearm"],
                wrist=form.cleaned_data["wrist"],
                bmi=calculate_bmi(
                    form.cleaned_data["weight"], form.cleaned_data["height"]
                ),
                bodyfat=predict_bodyfat(form.cleaned_data),
            )
            return redirect("dashboard:bodystats:show_latest")
        else:
            form = NewBodystatsForm(request.POST)
            return render(
                request, "dashboard/bodystats/add_bodystats.html", {"form": form}
            )
    form = NewBodystatsForm()
    return render(
        request, "dashboard/bodystats/add_bodystats.html", context={"form": form}
    )


def update_bodystats_view(request, id):
    pass


def delete_bodystats_view(request, id):
    pass
