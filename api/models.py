from django.db import models

# Create your models here.

# for later
# class DoctorData(models.Model):
#     name = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.name


class PatientData(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    gender = models.CharField(max_length=6)
    
    color = models.CharField(max_length=10)
    
    case = models.CharField(max_length=200)
    code = models.IntegerField()
    cost = models.IntegerField()
    paid_amount = models.IntegerField()
    monthly_rent = models.IntegerField(blank=True, null=True)
    
    next_appointment_date = models.DateField(blank=True, null=True)
    next_appointment_time = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class PatientImages(models.Model):
    patient = models.ForeignKey(PatientData, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    
    def __str__(self):
        return self.patient.name + "'s Image" 


class PatientVisits(models.Model):
    patient = models.ForeignKey(PatientData, on_delete=models.CASCADE, related_name='visits')
    visited_date = models.DateField()
    paid_amount = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.patient.name + "'s Visit"
    
    
