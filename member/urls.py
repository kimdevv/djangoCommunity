from django.urls import include, path
from .views import *
from . import views

app_name = 'member'

urlpatterns = [
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('login/', Login.as_view()),
    path('info/', Info.as_view()),
    path('post/', Post.as_view()),
]
