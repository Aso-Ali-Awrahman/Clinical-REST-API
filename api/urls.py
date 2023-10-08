from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('api/getPatientsData', views.getAllPatients),
    path('api/getPatientDetail/<str:id>', views.getOnePatient),
    
    path('api/createPatient', views.createPatient),
    path('api/uploadImages/<int:id>', views.uploadImages),
    
    path('api/updatePatient/<int:id>', views.updatePatientData)
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)