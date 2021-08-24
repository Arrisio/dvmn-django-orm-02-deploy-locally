import humanize
from datetime import timedelta
from django.utils.timezone import now, localtime
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved",
        )

    @property
    def duration(self):
        return localtime(self.leaved_at) - localtime(self.entered_at)

    @staticmethod
    def format_duration(duration):
        humanize.i18n.activate("ru_RU")
        return humanize.precisedelta(duration, minimum_unit="seconds", format="%0.0f", suppress=["days"])

    def is_visit_long(self, minutes=60):
        return self.duration > timedelta(minutes=minutes)
