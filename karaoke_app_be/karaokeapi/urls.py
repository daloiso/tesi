from django.urls import path

from karaokeapi import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter




router = DefaultRouter()
#router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile',views.UserProfileViewSet)

urlpatterns = [
    #path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
]