from django.contrib import admin
from django.urls import include, path
# from .views import ContactListView, ProfileView
from django.views.generic import TemplateView
from .views import BoardView, CurrencyRateView
from news.views import NewsListView, LawsListView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60*60)(BoardView.as_view()), name='dashboard'),
    path('rates', CurrencyRateView.as_view(), name='rates'),
    path('news', NewsListView.as_view(), name='news'),
    path('laws', LawsListView.as_view(), name='laws'),
    # path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]