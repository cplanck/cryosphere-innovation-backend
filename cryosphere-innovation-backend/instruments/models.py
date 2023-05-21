from django.db import models

from instruments.base_models import *


class AvailableInstruments(models.Model):
    name = models.CharField(max_length=200, null=True)
    internal = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Instrument(BaseInstrument):
    type = models.ForeignKey(AvailableInstruments,
                             on_delete=models.CASCADE, blank=True, null=True)


class Deployment(BaseDeployment):
    Instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, blank=True, null=True)
