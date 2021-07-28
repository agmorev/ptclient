# news/urls.py

from django.urls import path
from . import views


urlpatterns = [
    # News patterns
    path('', views.NewsListView.as_view(), name='news_list'),
    path('laws/', views.LawsListView.as_view(), name='laws_list'),
]
