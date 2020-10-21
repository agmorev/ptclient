from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.flatpage, {'url': '/home/'}, name='home'),
    path('orders/', include('orders.urls'), name='orders'),
]