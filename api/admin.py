from django.contrib import admin
from .models import PatientData, PatientImages, PatientVisits
# Register your models here.

admin.site.register(PatientData)
admin.site.register(PatientImages)
admin.site.register(PatientVisits)
