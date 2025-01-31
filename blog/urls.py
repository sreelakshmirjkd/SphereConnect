
from django.urls import path

from blog import views

from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns=[

    path("signup/", views.UserCreateView.as_view()),

    path("token/", ObtainAuthToken.as_view()),

    path("profile/", views.ProfileUpdateView.as_view()),

    path("user/", views.UserDetailView.as_view()),

    path("posts/", views.PostListCreateView.as_view()),

    path("posts/<int:pk>/", views.PostRetrieveUpdateDestroyView.as_view()),

    path("posts/<int:pk>/comments/", views.CommentCreateView.as_view()),

    path("posts/<int:pk>/add-like", views.PostLikeView.as_view()),
    

]