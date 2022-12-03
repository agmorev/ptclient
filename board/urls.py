from django.urls import path
from .views import BoardView, CurrencyRateView
from news.views import NewsListView, LawsListView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60*60)(BoardView.as_view()), name='dashboard'),
    path('rates', CurrencyRateView.as_view(), name='rates'),
    path('news', NewsListView.as_view(), name='news'),
    path('laws', LawsListView.as_view(), name='laws'),
]