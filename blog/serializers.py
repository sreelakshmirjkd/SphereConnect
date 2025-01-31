from django.contrib.auth.models import User

from rest_framework import serializers

from django.utils import timezone

from blog.models import Profile, Post, Comment


class UserSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField(read_only=True)


    class Meta:

        model = User

        fields = ["id", "username", "email", "password", "profile"]



    def create(self, validated_data):

        return User.objects.create_user(**validated_data)
    

    def get_profile(self, obj):

        profile_instance = Profile.objects.get(owner=obj) # query set 

        serializer_instance = ProfileSerializer(profile_instance, many=False) # serialization -- single profile so many=False

        return serializer_instance.data




class ProfileSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)

    greetings = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Profile

        fields = "__all__"

        read_only_fields = ["id", "owner"]
    

    def get_greetings(self, obj):

        return "Welcome..."

# This serializer put on the top for second method

class CommentSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only = True)

    post_object = serializers.StringRelatedField(read_only = True)
    

    class Meta:

        model = Comment

        fields = "__all__"

        read_only_fields = ["id", "owner", "post_object", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(read_only=True)

    # First method
    # ------------

    # comments = serializers.SerializerMethodField(read_only=True) # To add comments below each post

    # Second method --- CommentSerializer moved to top -- a method comments added to Post model.
    # -------------

    comments = CommentSerializer(read_only=True, many=True)

    comment_count = serializers.SerializerMethodField(read_only=True)

    like_count = serializers.SerializerMethodField(read_only=True)

    liked_by = serializers.StringRelatedField(read_only=True, many=True)

    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Post
        
        fields = "__all__"

        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def get_comments(self, obj):

        # comment_objects = Comment.objects.filter(post_object=obj) # --- child model 
        
        comment_objects = obj.post_comments.all() # using related name --- using parent object to get child

        serializer_instance = CommentSerializer(comment_objects, many=True)

        return serializer_instance.data
    
    def get_comment_count(self, obj):

        comment_count = obj.post_comments.all().count() # count is numnerical so, no need of serialization

        return comment_count
    
    def get_like_count(self, obj): # likes count for a user's post

        like_count = obj.liked_by.all().count()

        return like_count
    
    # serializer_context -- in PostListCreateView

    def get_is_liked(self, obj): # To check whether I/a user in his insta account have liked others' post or not.

        post_liked_users = obj.liked_by.all()

        # context = {"user":request.user}

        user = self.context.get("user")

        return user in post_liked_users





# liked_by -- request.user -- from url to views -- So, we need to move it to serializer.