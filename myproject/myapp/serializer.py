from rest_framework import serializers
from .models import mediafile, mediafiledata, logs

class mediafileserializer(serializers.ModelSerializer):
    """
    Serializer for handling the main media file.
    Using ModelSerializer simplifies the creation process for the mediafile model.
    """
    class Meta:
        model = mediafile
        fields = ['id', 'file']

class mediafiledataserializer(serializers.ModelSerializer):
    media_file = mediafileserializer()  # Nested serializer to include mediafile data
    uploaded_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = mediafiledata
        fields = ['media_file', 'name', 'size', 'extension', 'uploaded_by']

    def create(self, validated_data):
        """
        Creates a new mediafiledata entry in the database.
        """
        media_file_data = validated_data.pop('media_file')
        
        # Create the mediafile object first
        media_file = mediafile.objects.create(**media_file_data)
        
        user = self.context['request'].user
        
        # Now, create and return the mediafiledata object
        return mediafiledata.objects.create(media_file=media_file, uploaded_by=user, **validated_data)
    
class logserializer(serializers.ModelSerializer):
    class Meta:
        model=logs
        fields=['media_file_data','before_data','after_data','timestamp']