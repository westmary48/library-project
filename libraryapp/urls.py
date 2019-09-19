from django.conf.urls import url
from django.conf.urls import url, include
from .views import *

app_name = "libraryapp"

urlpatterns = [
    url(r'^home$', book_list, name='home'),
    url(r'^books$', book_list, name='books'),
    url(r'^librarians$', list_librarians, name='librarians'),
    url(r'^libraries$', list_library, name='libraries'),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^book/form$', book_form, name='book_form'),
]
