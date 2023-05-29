from django.contrib import admin

from .models import *


# Register your models here.
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'instrument_type']


class DeploymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'instrument', 'deployment_number', 'status']


admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Deployment, DeploymentAdmin)
