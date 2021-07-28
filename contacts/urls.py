from django.contrib import admin
from django.urls import include, path
from .views import ContactListView, ProfileView

urlpatterns = [
    path('', ContactListView.as_view(), name='contacts'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]