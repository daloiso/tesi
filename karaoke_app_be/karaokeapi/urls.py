from django.urls import path

from karaokeapi import views


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
]