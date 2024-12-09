from rest_framework import serializers
from karaokeapi import models
from karaokeapi.models import TeachingActivities, KeyWordSong


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingActivities
        fields = ['title', 'fileMp3Name', 'fileMp3', 'textSong',]

class KeyWordSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWordSong
        fields = ['word', 'wordsToDisplay', 'imageName', 'image','wordSyntetized','time_word','teachingActivity']

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)