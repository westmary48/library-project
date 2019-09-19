from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from libraryapp.models import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('libraryapp.urls')),
]
