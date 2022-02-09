"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include('conduit.apps.articles.urls', namespace='articles')),
    url(r'^api/', include('conduit.apps.authentication.urls', namespace='authentication')),
    url(r'^api/', include('conduit.apps.profiles.urls', namespace='profiles')),]
