from rest_framework import serializers
from .models import PatientData, PatientImages


class PatientImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientImages
        fields = ['image', 'patient']  # we must use all for the create serializer

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class PatientSerializer(serializers.ModelSerializer):
    images = PatientImageSerializer(many=True, read_only=True)
        
    class Meta:
        model = PatientData
        fields = '__all__'
        