from django.urls import path

from karaokeapi import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register('profile',views.UserProfileViewSet)


urlpatterns = [
    #path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('activity/', views.ActivityView.as_view(), name='activity_view'),  # Map the URL to the view

    path('', include(router.urls)),
]