from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import mediafiledata,logs
from .serializer import mediafiledataserializer, mediafileserializer,logserializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated

class Mediafileuploadview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"file": ["No file was submitted."]}, status=status.HTTP_400_BAD_REQUEST)

        media_file_serializer = mediafileserializer(data={"file": file})
        if media_file_serializer.is_valid():
            media_file = media_file_serializer.save(uploaded_by=request.user)

            media_file_data = {
                "media_file": media_file.id,  # Pass mediafile ID
                "name": file.name,
                "size": file.size,
                "extension": file.name.split('.')[-1],
                "uploaded_by": request.user.id,  # Pass user ID
            }

            media_file_data_serializer = mediafiledataserializer(data=media_file_data)
            if media_file_data_serializer.is_valid():
                media_file_data_serializer.save()
                return Response(
                    {"message": "File and associated data saved successfully"},
                    status=status.HTTP_201_CREATED
                )
            return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(media_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        if pk:
            try:
                media_file = mediafiledata.objects.get(pk=pk)
                serializer = mediafiledataserializer(media_file)
                Logs=logs.objects.filter(media_file_data=media_file)
                Logs_serializer=logserializer(Logs,many=True)
                return Response({
                    'mediafiledata': serializer.data,
                    'change_logs': Logs_serializer.data,
                    'uploaded_by':media_file.uploaded_by.username
                    },status=status.HTTP_200_OK)
            except mediafiledata.DoesNotExist:
                return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        media_files = mediafiledata.objects.all()
        serializer = mediafiledataserializer(media_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        try:
            media_file = mediafiledata.objects.get(pk=pk,uploaded_by=request.user)
        except mediafiledata.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        media_file_data_serializer = mediafiledataserializer(media_file, data=request.data)
        if media_file_data_serializer.is_valid():
            media_file_data_serializer.save()
            return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)

        return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            media_file = mediafiledata.objects.get(pk=pk,uploaded_by=request.user)
        except mediafiledata.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        before_data=mediafiledataserializer(media_file).data

        media_file_data_serializer = mediafiledataserializer(media_file, data=request.data, partial=True)
        if media_file_data_serializer.is_valid():
            media_file_data_serializer.save()

            after_data=mediafiledataserializer(media_file).data
            
            logs.objects.create(
                media_file_data=media_file,
                before_data=before_data,
                after_data=after_data,
            )

            return Response({"message": "Data successfully updated"}, status=status.HTTP_200_OK)

        return Response(media_file_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            media_file = mediafiledata.objects.get(pk=pk,uploaded_by=request.user)
        except mediafiledata.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        media_file.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class registerview(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({"error":"user already created"},status=400)
        user=User.objects.create_user(username=username,email=email,password=password)
        return Response({"message":"user created"},status=status.HTTP_201_CREATED)
    
class loginview(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        user= authenticate(username=username,password=password)
        if user:
            refresh=RefreshToken.for_user(user)
            return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        return Response({"error":"invaid"},status=status.HTTP_401_UNAUTHORIZED)
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