from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    this_passcard_visits = [
        {
            "entered_at": localtime(visit.entered_at),
            "duration": visit.format_duration(visit.duration),
            "is_strange": visit.is_visit_long(),
        }
        for visit in Visit.objects.filter(passcard=passcard)
    ]
    context = {"passcard": passcard, "this_passcard_visits": this_passcard_visits}
    return render(request, "passcard_info.html", context)
