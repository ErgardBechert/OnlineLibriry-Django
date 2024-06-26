"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterUser.as_view(), name='register'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)), #RedirectView  принимает первым параметром новый относительный URL на который следует перенаправлять (/catalog/) когда указанный в функции url() адрес соотносится с адресом запроса (корневой URL, в данном случае).
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [path('catalog/', include('catalog.urls'))]  

