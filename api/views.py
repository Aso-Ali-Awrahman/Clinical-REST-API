from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser


from pprint import pprint

from .models import PatientData, PatientVisits, PatientImages
from .serializers import PatientSerializer, PatientImageSerializer, PatientVisitsSerializer


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
    
    patient = request.data['patient_data']
    
    patient_visits = request.data['patient_visits']
    
    patient_serializer = PatientSerializer(data=patient)
    
    if patient_serializer.is_valid():
        patient = patient_serializer.save()
        
        for visit_json in patient_visits:
            visit_json['patient'] = patient.id
            visit_serializer = PatientVisitsSerializer(data=visit_json)
            if visit_serializer.is_valid():
                visit_serializer.save()
    
    return Response(patient.id, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def uploadImages(request, id): 
    
    for file in request.FILES.values():
        
        serializer = PatientImageSerializer(data={'image': file, 'patient': id})
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def updatePatientData(request, id):
    try:
        patient_old = PatientData.objects.get(pk=id)
        patient_visits = PatientVisits.objects.filter(patient=id)
    except PatientData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    patient_to_update = request.data['patient_data']
    
    # patient_visits_to_update = request.data['patient_visits']
    print(patient_visits)
    patient_serializer = PatientSerializer(patient_old, patient_to_update)
    
    if patient_serializer.is_valid():
        patient_serializer.save()
    
    # patient_visits_serializer = PatientVisitsSerializer(patient_visits_to_update)
    
    return Response(status=status.HTTP_202_ACCEPTED)