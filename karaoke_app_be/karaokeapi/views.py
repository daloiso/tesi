from io import BytesIO

from gtts import gTTS
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from karaokeapi import serializer
from karaokeapi import models
from karaokeapi import permission
from karaokeapi.models import KeyWordSong
from karaokeapi.serializer import ActivitySerializer, KeyWordSongSerializer
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializer.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')
    #def perform_create(self, serializer):
    #   serializer.save(user_profile=self.request.user)

class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]  # Use Token Authentication
    permission_classes = [IsAuthenticated, permission.OnlyMe]  # Only authenticated users can access

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user.id
        teaching_activities = models.UserProfile.objects.get_teachings(user)
        serializer1 = ActivitySerializer(teaching_activities, many=True)
        return Response(serializer1.data, status=status.HTTP_200_OK)

    def post(self,request):
        #user = request.user

        #if user.username != 'pasquale.daloiso@gmail.com':
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Apply the custom permission
        permission1 = permission.OnlyMe()
        if not permission1.has_object_permission(request, None, None):
            return Response({"detail": "You do not have permission to create a product."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer1 = ActivitySerializer(data=request.data)

        if serializer1.is_valid():
            serializer1.save()
            return Response(serializer1.data, status=status.HTTP_201_CREATED)
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)



class VerseView(APIView):
    authentication_classes = [TokenAuthentication]  # Use Token Authentication
    permission_classes = [IsAuthenticated, permission.OnlyMe]  # Only authenticated users can access

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user.id
        teaching_activities = models.UserProfile.objects.get_teachings(user)
        title = request.GET.get('title')

        filtered_activities = teaching_activities.filter(title=title)
        activity_exists = filtered_activities.exists()
        if activity_exists:
            keywords = KeyWordSong.objects.get_music(filtered_activities[0].id)
            serializer1 = KeyWordSongSerializer(keywords, many=True)
            return Response(serializer1.data, status=status.HTTP_200_OK)
        return  Response({"detail": "You do not have permission to get a product."},
                            status=status.HTTP_403_FORBIDDEN)

    def post(self,request):
        #user = request.user

        #if user.username != 'pasquale.daloiso@gmail.com':
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Apply the custom permission
        permission1 = permission.OnlyMe()
        if not permission1.has_object_permission(request, None, None):
            return Response({"detail": "You do not have permission to create a product."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer1 = KeyWordSongSerializer(data=request.data)

        if serializer1.is_valid():
            serializer1.save()
            return Response(serializer1.data, status=status.HTTP_201_CREATED)
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class FilesView(APIView):
    authentication_classes = [TokenAuthentication]  # Use Token Authentication
    permission_classes = [IsAuthenticated, permission.OnlyMe]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user.id
        title = request.GET.get('title')
        stream = request.GET.get('stream')
        type_parameter = request.GET.get('type')
        index = request.GET.get('index')

        teaching_activities = models.UserProfile.objects.get_teachings(user)
        filtered_activities = teaching_activities.filter(title=title)
        activity_exists = filtered_activities.exists()
        if activity_exists:

            if type_parameter=='mp3':

                file_path = os.path.join(settings.MEDIA_ROOT, 'activities/'+filtered_activities[0].fileMp3Name)
                if os.path.exists(file_path):
                    # Open the file in binary mode
                    file = open(file_path, 'rb')  # Don't use 'with' here to prevent it from closing immediately
                    # Pass the file object to FileResponse
                    response = FileResponse(file)
                    if stream:
                        response['Content-Type'] = 'audio/mpeg'
                    response['Content-Disposition'] = f'attachment; filename="{filtered_activities[0].fileMp3Name}"'
                    return response
                else:
                    return Response({"detail": "file not found"},
                        status=status.HTTP_404_NOT_FOUND)
            if type_parameter=='img':
                keywords = KeyWordSong.objects.get_music(filtered_activities[0].id)
                file_path = keywords[int(index)].image.path
                if os.path.exists(file_path):
                    # Open the file in binary mode
                    file = open(file_path, 'rb')  # Don't use 'with' here to prevent it from closing immediately
                    # Pass the file object to FileResponse
                    response = FileResponse(file)
                    if stream:
                        response['Content-Type'] = 'image/png'
                    response['Content-Disposition'] = f'attachment; filename="{keywords[int(index)].imageName}"'
                    return response
                else:
                    return Response({"detail": "file not found"},
                                    status=status.HTTP_404_NOT_FOUND)
            if type_parameter == 'word':
                keywords = KeyWordSong.objects.get_music(title)
                file_path = os.path.join(settings.MEDIA_ROOT, keywords[index].wordSyntetized)
                if os.path.exists(file_path):
                    # Open the file in binary mode
                    file = open(file_path, 'rb')  # Don't use 'with' here to prevent it from closing immediately
                    # Pass the file object to FileResponse
                    response = FileResponse(file)
                    if stream:
                        response['Content-Type'] = 'audio/mpeg'
                    response['Content-Disposition'] = f'attachment; filename="{keywords[index].wordSyntetized}"'
                    return response
                else:
                    return Response({"detail": "file not found"},
                                    status=status.HTTP_404_NOT_FOUND)
            if type_parameter == 'sentence':
                text = request.GET.get("sentencePar", None)
                if not text:
                    return Response({"error": "No sentence provided"}, status=status.HTTP_400_BAD_REQUEST)

                # Generate speech using gTTS
                tts = gTTS(text=text, lang='it')

                # Save speech to a bytes buffer instead of a file
                mp3_file = BytesIO()
                tts.write_to_fp(mp3_file)
                mp3_file.seek(0)

                # Return the speech as an MP3 file
                response = HttpResponse(mp3_file, content_type="audio/mpeg")
                response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
                return response

        else:
            return Response({"detail": "you don't have the permission."},
                                status=status.HTTP_401_UNAUTHORIZED)
        return Response({"detail": "wrong parameters"},
                        status=status.HTTP_401_UNAUTHORIZED)


class RichiesteView(APIView):
    authentication_classes = [TokenAuthentication]  # Use Token Authentication
    permission_classes = [IsAuthenticated, permission.OnlyMe]
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        email = request.data.get('email')
        firstName = request.data.get('firstName')
        lastName = request.data.get('lastName')
        message = request.data.get('message')
        genereMusicale = request.data.get('genereMusicale')
        //karaoke4all_01!
        //karaoke4all.ddns.net@gmail.com

        return Response('OK', status=status.HTTP_200_OK)