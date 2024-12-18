from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import mediaFile, mediaFileData, logs
from .serializer import mediafiledataserializer, mediafileserializer, logserializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .tasks import save_media_file_properties
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
class Mediafileuploadview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
    # Extract the file from the request
        file = request.FILES.get('file')
        if not file:
            return Response({"file": ["No file was submitted."]}, status=status.HTTP_400_BAD_REQUEST)

    # Step 1: Create mediafile instance with the uploaded file
        media_file = mediaFile.objects.create(
            file=file,
            uploaded_by=request.user  # Assign the current logged-in user
        )

    # Step 2: Prepare initial data for mediaFileData
        properties_available_at = timezone.now() + timedelta(minutes=5)
        properties_available_at = timezone.localtime(timezone.now() + timedelta(minutes=5))
        # readable_time = properties_available_at.strftime("%B %d, %Y, %I:%M %p")
        media_file_data = {
            "media_file": media_file.id,  # Reference to the media file
            "properties_available_at": properties_available_at,
            "uploaded_by": request.user
        }

    # Step 3: Save the mediafiledata (do NOT pass uploaded_by here)
        media_file_data_serializer = mediafiledataserializer(data=media_file_data, context={"request": request})
        if media_file_data_serializer.is_valid():
        # Save the media file data (DO NOT pass uploaded_by as it's already set in the media file model)
            media_file_data_serializer.save()

        # # Step 4: Schedule the Celery task
        #     save_media_file_properties.apply_async( 
        #         args=[media_file_data_serializer.instance.id],
        #         countdown=5 * 60  # Delay of 5 minutes
        #     )
            # formatted_time = properties_available_at.strftime("%B %d, %Y, %I:%M %p")
        # Step 5: Return a success response    in 7 lines ki jagah mn ne yeh nechay ek line likhi just
        # function name aur parameeter pass kr dia
            save_media_file_properties.delay(media_file_data_serializer.instance.id)
            return Response(
                {
                    "message": "File uploaded successfully.",
                    "id": media_file_data_serializer.instance.id,
                    "properties_available_at": datetime.datetime.now()
                },
                status=status.HTTP_201_CREATED
            )
        else:
        # Rollback if validation fails
            media_file.delete()
            return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def get(self, request, pk=None):
        if pk:
            try:
                # Retrieve the media file data
                media_file_data = mediaFileData.objects.get(pk=pk)
                # Check if the properties have been processed
                if not media_file_data.name:  # Properties not extracted yet
                    formatted_time = media_file_data.properties_available_at.strftime("%B %d, %Y, %I:%M %p")
                    return Response({
                    'properties_available_at': formatted_time
                }, status=status.HTTP_200_OK)

                # Return the media file data with properties
                return Response({
                    "media_file": media_file_data.media_file.id,
                    "name": media_file_data.name,
                    "size": media_file_data.size,
                    "extension": media_file_data.extension,
                    "uploaded_by": media_file_data.uploaded_by.username
                }, status=status.HTTP_200_OK)

            except mediaFileData.DoesNotExist:
                return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        # For listing all media files
        media_files = mediaFileData.objects.all()
        serializer = mediafiledataserializer(media_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        try:
            # Ensure the user is authorized to update the record
            media_file = mediaFileData.objects.get(pk=pk, uploaded_by=request.user)
        except mediaFileData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        media_file_data_serializer = mediafiledataserializer(media_file, data=request.data)
        if media_file_data_serializer.is_valid():
            media_file_data_serializer.save()
            return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)

        return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            media_file = mediaFileData.objects.get(pk=pk, uploaded_by=request.user)
        except mediaFileData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        before_data = mediafiledataserializer(media_file).data

        media_file_data_serializer = mediafiledataserializer(media_file, data=request.data, partial=True)
        if media_file_data_serializer.is_valid():
            media_file_data_serializer.save()

            after_data = mediafiledataserializer(media_file).data

            # Create a log entry for the changes
            logs.objects.create(
                media_file_data=media_file,
                before_data=before_data,
                after_data=after_data,
            )

            return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)

        return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            # Ensure the user is authorized to delete the record
            media_file = mediaFileData.objects.get(pk=pk, uploaded_by=request.user)
        except mediaFileData.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        media_file.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class registerview(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)


class loginview(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class logoutview(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({'message': 'Logout successful'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)