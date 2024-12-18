from rest_framework import serializers
from .models import mediaFile, mediaFileData, logs

class mediafileserializer(serializers.ModelSerializer):
    class Meta:
        model = mediaFile
        fields = ['id', 'file']

class mediafiledataserializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')  # Read-only field for response

    class Meta:
        model = mediaFileData
        fields = ['media_file', 'name', 'size', 'extension', 'uploaded_by', 'properties_available_at']

    def create(self, validated_data):
        # Assign the uploaded_by user from the request context
        uploaded_by = self.context['request'].user
        return mediaFileData.objects.create(uploaded_by=uploaded_by, **validated_data)
class logserializer(serializers.ModelSerializer):
    class Meta:
        model = logs
        fields = ['media_file_data', 'before_data', 'after_data', 'timestamp']
