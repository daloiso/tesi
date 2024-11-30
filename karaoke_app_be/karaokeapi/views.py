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
from karaokeapi.serializer import ActivitySerializer


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

        return Response({'message': 'You are authenticated!'})

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
