from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import now, localtime


def storage_information_view(request):
    non_closed_visits = [
        {
            "who_entered": visit.passcard.owner_name,
            "entered_at": localtime(visit.entered_at),
            "duration": visit.format_duration(visit.duration),
        }
        for visit in Visit.objects.filter(leaved_at__isnull=True)
    ]
    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, "storage_information.html", context)
