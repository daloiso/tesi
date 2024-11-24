from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user




class TeachingActivities(models.Model):
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    textSong = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class KeyWordSong(models.Model):
    word = models.CharField(max_length=200)
    imagePath=models.CharField(max_length=200)
    time_word = models.TimeField()
    teachingActivity = models.ForeignKey(TeachingActivities, on_delete=models.CASCADE, related_name='keyWordSongs')

    def __str__(self):
        return self.word

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    teachingActivities = models.ManyToManyField(TeachingActivities, related_name='activities')
    #teachingActivities = up.teachingActivities.all()

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


