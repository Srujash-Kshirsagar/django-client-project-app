from rest_framework import serializers
from .models import Client, Project

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)  # Get the username

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user  # Set the logged-in user
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user  # Set the logged-in user
        return super().create(validated_data)
