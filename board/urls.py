from django.urls import path
from .views import *
from . import views

app_name = 'board'

urlpatterns = [
    path('', PostAPIs.as_view()),
    path('<int:post_id>/', DetailAPIs.as_view()),
    path('<int:post_id>/comment/', CommentAPIs.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/', DeleteComment.as_view()),
    path('univ/<str:university_name>/', PostByUnivAPIs.as_view()),
]
