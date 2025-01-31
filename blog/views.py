from django.shortcuts import render

# Create your views here.

from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.serializers import UserSerializer

from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib.auth.models import User

from rest_framework import authentication, permissions

from blog.models import Profile, Post

from blog.serializers import ProfileSerializer, PostSerializer, CommentSerializer

from django.shortcuts import get_object_or_404




class UserCreateView(CreateAPIView):

    serializer_class = UserSerializer


class ProfileUpdateView(UpdateAPIView, RetrieveAPIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ProfileSerializer

    def get_object(self): # same def for update and retrieve

        profile_instance = Profile.objects.get(owner=self.request.user)

        return profile_instance



class UserDetailView(RetrieveAPIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer

    def get_object(self):

        user_instance = User.objects.get(username=self.request.user) # user who send the token

        return user_instance
    

class PostListCreateView(ListCreateAPIView):

    queryset = Post.objects.all()

    serializer_class = PostSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer): # overriding -- while inheriting from createapiview or listcreateapiview.

        serializer.save(owner=self.request.user)
    
   # To check whether I/a user in his insta account have liked others' post or not.
    
    def get_serializer_context(self): # Overriding - we need to pass request.user to serializer -- serializer_class = PostSerializer

        context = super().get_serializer_context() # super - to refer parent class, self - to refer current instance

        context["user"] = self.request.user # overriding to add an extra key

        return context
    

class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer

    queryset = Post.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]


# class CommentCreateView(APIView):

#     serializer_class = CommentSerializer

#     authentication_classes = [authentication.TokenAuthentication]

#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):

#         id = kwargs.get("pk")

#         post_instance = Post.objects.get(id=id)

#         serializer_instance = self.serializer_class(data=request.data) # data ={"message"}

#         if serializer_instance.is_valid():

#             serializer_instance.save(owner=request.user, post_object=post_instance)

#             return Response(data=serializer_instance.data)
        
#         else:

#             return Response(data=serializer_instance.errors)
        

class CommentCreateView(CreateAPIView):

    serializer_class = CommentSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer): # overriding to add two more fields' data

        id = self.kwargs.get("pk")

        post_instance = Post.objects.get(id=id)

        serializer.save(owner=self.request.user, post_object = post_instance)
    

class PostLikeView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        id = kwargs.get("pk")

        post_object = get_object_or_404(Post, id=id)

        liked_users = post_object.liked_by.all()

        if request.user in liked_users:

            post_object.liked_by.remove(request.user)

        else:

            post_object.liked_by.add(request.user)
        
        post_object.liked_by.add(request.user) # adding a user a ManyToMany field

        return Response(data={"message": "liked"})





    