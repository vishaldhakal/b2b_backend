from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, Attendee
# Register your models here.

admin.site.register(Event,ModelAdmin)
admin.site.register(Attendee,ModelAdmin)