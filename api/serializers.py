from rest_framework import serializers
from .models import PatientData, PatientImages, PatientVisits


class PatientImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientImages
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)



class PatientVisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVisits
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    images = PatientImageSerializer(many=True, read_only=True)
    visits = PatientVisitsSerializer(many=True, read_only=True) 
        
    class Meta:
        model = PatientData
        fields = '__all__'
        