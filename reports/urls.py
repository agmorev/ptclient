from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('report/general/', views.GeneralReportView.as_view(), name='report'),
]