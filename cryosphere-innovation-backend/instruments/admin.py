from django.contrib import admin

from .models import *


# Register your models here.
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'type']


admin.site.register(AvailableInstruments)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Deployment)
