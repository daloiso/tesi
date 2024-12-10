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

    def get_teachings(self, iduser):
        user = self.model(id=iduser)
        return user.teachingActivities



class MusicManager(models.Manager):
    """Manager for music"""

    def get_music(self, id_teaching):
        return self.filter(teachingActivity=id_teaching).order_by('time_word')

class TeachingActivities(models.Model):
    title = models.CharField(max_length=200,  unique=True)
    fileMp3Name = models.CharField(max_length=200)
    fileMp3 = models.FileField(upload_to='activities/')
    textSong = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class KeyWordSong(models.Model):
    word = models.CharField(max_length=200, unique=True)
    wordsToDisplay = models.CharField(max_length=200)
    imageName=models.CharField(max_length=200)
    image = models.FileField(upload_to='keywordsImage/')
    time_word = models.IntegerField()
    teachingActivity = models.ForeignKey(TeachingActivities, on_delete=models.CASCADE, related_name='keyWordSongs')
    objects = MusicManager()

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


