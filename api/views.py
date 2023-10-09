from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser

import pandas as pd
import os
import shutil
from random import randint

from .models import PatientData, PatientImages
from .serializers import PatientSerializer, PatientImageSerializer



# Create your views here.

@api_view(['GET'])
def getAllPatients(request): 
    patients = PatientData.objects.all()
    
    if len(patients) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = PatientSerializer(patients, many=True, context={'request': request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def getOnePatient(request, id):
    try:
        patient = PatientData.objects.get(pk=id)
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PatientSerializer(patient, many=False, context={'request': request})
    
    return Response(serializer.data)



@api_view(['POST'])
def createPatient(request):
    
    patient_serializer = PatientSerializer(data=request.data)
    
    if patient_serializer.is_valid():
        patient = patient_serializer.save()
        return Response({"patient id": patient.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@parser_classes([MultiPartParser])
def uploadImages(request, id): 
    
    try:
        PatientData.objects.get(pk=id) # check if the patient is exist to link it with images
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    for file in request.FILES.values():
        
        serializer = PatientImageSerializer(data={'image': file, 'patient': id})
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def exportData(request, password):
    if password != "AdminBase":
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    patients = PatientData.objects.all()
    
    try:
        data_list = list(patients.values())  # make the data object to a list so that pd can read it
        df = pd.DataFrame(data_list)  
        
        desktop_directory = os.path.join(os.path.expanduser("~"), f"Desktop/Clinic Data{randint(1, 1000)}")  # simply gets the user desktop directory
        os.makedirs(desktop_directory, exist_ok=True)
        
        excel_file_path = os.path.join(desktop_directory, f"Patients Data.xlsx") # create the excel folder
    
        df.to_excel(excel_file_path, index=False)  # save the data in the excel
        
        # copy the media folder to the desktop
        media_directory = "C:/Users/TOTAL TECH CO/Desktop/Visual code/RestFrame/media"
        shutil.copytree(media_directory, os.path.join(desktop_directory, "Media"))
        
    except Exception as e:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    
    return Response(status=status.HTTP_201_CREATED)
    


@api_view(['PUT'])
def updatePatientData(request, id):
    try:
        patient_old = PatientData.objects.get(pk=id)
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    patient_to_update = request.data
    
    patient_serializer = PatientSerializer(patient_old, patient_to_update)
    
    if patient_serializer.is_valid():
        patient_serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['DELETE'])
def deletePatientData(request, id):
    try:
        patient = PatientData.objects.get(pk=id)
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    patient.delete()
    
    return Response(status=status.HTTP_204_NO_CONTENT)

