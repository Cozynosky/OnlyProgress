from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bodystats_predictor.bodystats_operations import (
    calculate_bmi,
    get_weight_status,
    get_bodyfat_status,
    estimate_bodyfat,
)
from bodystats_predictor.predictors import predict_bodyfat
from .forms import BodystatsForm
from .models import BodyStats, UNITS


def latest_bodystats_view(request):
    try:
        pk = request.user.profile.bodystats_set.last().pk
    except Exception:
        pk = 0
    return redirect("dashboard:bodystats:show_bodystats", id=pk)


def show_bodystats_view(request, id=1):
    try:
        bodystats_set = BodyStats.objects.get(pk=id)

        creation_time = bodystats_set.date
        bmi = {"val": bodystats_set.bmi, "status": get_weight_status(bodystats_set.bmi)}
        predicted_bodyfat = {
            "val": bodystats_set.bodyfat,
            "status": get_bodyfat_status(
                bodystats_set.bodyfat, bodystats_set.profile.sex
            ),
        }
        estimated_bf = estimate_bodyfat(
            bodystats_set.bmi, bodystats_set.age, bodystats_set.profile.sex
        )
        estimated_bodyfat = {
            "val": estimated_bf,
            "status": get_bodyfat_status(estimated_bf, bodystats_set.profile.sex),
        }
        id = bodystats_set.pk

        bodystats = {
            "age": {"val": bodystats_set.age},
            "weight": {"val": bodystats_set.weight},
            "height": {"val": bodystats_set.height},
            "neck": {"val": bodystats_set.neck},
            "chest": {"val": bodystats_set.chest},
            "abdomen": {"val": bodystats_set.abdomen},
            "hip": {"val": bodystats_set.hip},
            "thigh": {"val": bodystats_set.thigh},
            "knee": {"val": bodystats_set.knee},
            "ankle": {"val": bodystats_set.ankle},
            "biceps": {"val": bodystats_set.biceps},
            "forearm": {"val": bodystats_set.forearm},
            "wrist": {"val": bodystats_set.wrist},
        }

        for stat_name, cont in bodystats.items():
            cont["unit"] = UNITS[stat_name]

        if len(request.user.profile.bodystats_set.all()) > 1:
            all_bodystats = list(request.user.profile.bodystats_set.all())
            current_bodystats_id = all_bodystats.index(bodystats_set)

            if current_bodystats_id != 0:
                curr = model_to_dict(all_bodystats[current_bodystats_id])
                prev = model_to_dict(all_bodystats[current_bodystats_id - 1])

                for stat_name in bodystats:
                    if curr[stat_name] > prev[stat_name]:
                        bodystats[stat_name]["change"] = "more"
                    elif curr[stat_name] < prev[stat_name]:
                        bodystats[stat_name]["change"] = "less"
                    else:
                        bodystats[stat_name]["change"] = "same"

        context = {
            "date": creation_time,
            "bmi": bmi,
            "predicted_bodyfat": predicted_bodyfat,
            "estimated_bodyfat": estimated_bodyfat,
            "bodystats": bodystats,
            "id": id,
        }

    except BodyStats.DoesNotExist:
        context = None

    return render(request, "dashboard/bodystats/show_bodystats.html", context=context)


def history_bodystats_view(request, page):
    all_stats = request.user.profile.bodystats_set.all().order_by("-date")
    paginator = Paginator(all_stats, 10)
    tens = paginator.count - 10 * (page - 1)

    try:
        stats = paginator.page(page)
    except PageNotAnInteger:
        stats = paginator.page(1)
    except EmptyPage:
        stats = paginator.page(paginator.num_pages)

    context = {"stats": stats, "tens": tens}

    return render(request, "dashboard/bodystats/show_history.html", context=context)


def add_bodystats_view(request, fill):
    if request.method == "POST":
        form = BodystatsForm(request.POST)
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
            form = BodystatsForm(request.POST)
            return render(
                request, "dashboard/bodystats/add_bodystats.html", {"form": form}
            )

    elif fill == "true":
        try:
            lastest_bodystats = model_to_dict(request.user.profile.bodystats_set.last())
            lastest_bodystats["date"] = now()

            form = BodystatsForm(initial=lastest_bodystats)
        except Exception:
            form = BodystatsForm()
    else:
        form = BodystatsForm(initial={"date": now()})
    return render(
        request, "dashboard/bodystats/add_bodystats.html", context={"form": form}
    )


def edit_bodystats_view(request, id):
    if request.method == "POST":
        form = BodystatsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["date"])
            bodystats_set = BodyStats.objects.get(pk=id)
            bodystats_set.date = form.cleaned_data["date"]
            bodystats_set.age = form.cleaned_data["age"]
            bodystats_set.weight = form.cleaned_data["weight"]
            bodystats_set.height = form.cleaned_data["height"]
            bodystats_set.neck = form.cleaned_data["neck"]
            bodystats_set.chest = form.cleaned_data["chest"]
            bodystats_set.abdomen = form.cleaned_data["abdomen"]
            bodystats_set.hip = form.cleaned_data["hip"]
            bodystats_set.thigh = form.cleaned_data["thigh"]
            bodystats_set.knee = form.cleaned_data["knee"]
            bodystats_set.ankle = form.cleaned_data["ankle"]
            bodystats_set.biceps = form.cleaned_data["biceps"]
            bodystats_set.forearm = form.cleaned_data["forearm"]
            bodystats_set.wrist = form.cleaned_data["wrist"]
            bodystats_set.bmi = calculate_bmi(
                form.cleaned_data["weight"], form.cleaned_data["height"]
            )
            bodystats_set.bodyfat = predict_bodyfat(form.cleaned_data)
            bodystats_set.save()
            return redirect("dashboard:bodystats:show_bodystats", id=id)
        else:
            form = BodystatsForm(request.POST)
            return render(
                request,
                "dashboard/bodystats/update_bodystats.html",
                context={"form": form},
            )
    else:
        try:
            bodystats_set = BodyStats.objects.get(pk=id)
            initial_dict = model_to_dict(bodystats_set)
            form = BodystatsForm(initial=initial_dict)
        except BodyStats.DoesNotExist:
            form = BodystatsForm()
    return render(
        request, "dashboard/bodystats/update_bodystats.html", context={"form": form}
    )


def delete_bodystats_view(request, id):
    try:
        stats = BodyStats.objects.get(pk=id)
        stats.delete()
    except BodyStats.DoesNotExist:
        pass
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def show_bodystat_chart_view(request, stat_name, page):
    all_stats = request.user.profile.bodystats_set.values("date", stat_name, "pk").order_by("-date")
    paginator = Paginator(all_stats, 10)
    
    try:
        stats = paginator.page(page)
    except PageNotAnInteger:
        stats = paginator.page(1)
    except EmptyPage:
        stats = paginator.page(paginator.num_pages)

    vals = []
    dates = []
    pks = []

    for stat in reversed(stats):
        dates.append(stat["date"])
        vals.append(float(stat[stat_name]))
        pks.append(stat["pk"])
        
    list_for_table = zip(reversed(dates), reversed(vals), reversed(pks))
    
    dates = list(map(lambda x: x.strftime("%d/%m/%Y"), dates))

    
    context = {"unit": f"{UNITS[stat_name]}", "labels": dates, "data": vals, "stat_name": stat_name, "stats": stats, "list_for_table": list_for_table}

    return render(
        request, "dashboard/bodystats/show_bodystat_chart.html", context=context
    )
