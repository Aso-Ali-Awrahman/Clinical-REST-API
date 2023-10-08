from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser


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

