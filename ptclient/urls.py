import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.conf.urls.static import static
from ptclient import settings

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls, name='admin'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.flatpage, {'url': '/home/'}, name='home'),
    path('calcs/', views.flatpage, {'url': '/calcs/'}, name='calcs'),
    path('orders/', include('orders.urls'), name='orders'),
    path('contacts/', include('contacts.urls'), name='contacts'),
    path('dashboard/', include('board.urls'), name='dashboard'),
    path('news/', include('news.urls')),
    path('references/', include('references.urls'), name='references'),
    path('forum/', include('posts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)