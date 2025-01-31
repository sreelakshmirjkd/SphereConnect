from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Profile(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")

    address = models.TextField(null=True)

    phone = models.CharField(max_length=15,null=True)

    GENDER_CHOICES = (

        ("male", "male"),
        ("female", "female")

    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="male")

    picture = models.ImageField(upload_to="profilepics", null=True, blank=True, default="profilepics/default.png")

    bio = models.CharField(max_length=100, null=True)

    # To create a profile when a user object is created and saved in User model i.e., after basic registration

    # signals -- post_save(), pre_save(), pre_init(), post_init(), pre_delete(), post_delete() --import after object creates

    # sender -- model where object save, instance -- object, created -- Boolean

    def create_profile(sender, instance, created, **kwargs):

        if created:

            Profile.objects.create(owner=instance)

    from django.db.models.signals import post_save  # importing signals

    post_save.connect(create_profile, User)


class Post(models.Model):

    caption = models.CharField(max_length=200)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")

    picture = models.ImageField(upload_to="postpictures", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    liked_by = models.ManyToManyField(User, related_name="posts") # For MAnyToMany, django creates a separate model. This field is not shown in blog_post model

    def comments(self):

        # return self.post_comments.all() # using parent -- here self. is used for post_object 
    
        return Comment.objects.filter(post_object=self) # using child 
    
    def __str__(self):

        return self.caption


# ForeignKey - OneToMany
# ==========

# single parent -- multiple child

# P1, P2, P3 -- Parent (Post objects created by different users and at different time)  --- C1, C2, C3 (Comment objects created by different users)

# class CommentModel:

# post_object = models.ForeignKey(Post, ...)

# P1 --> C1, C2 - no same comment for different posts -- not ManyToMany
# P2 --> C3, C4

# ------------------------------------------------------------------------

# Many to Many
# ============

# multiple parent -- multiple child

# Genres - G1, G2, G3 -- Parent    Movies - M1, M2, M3, M4

# class MovieModel:

# G1 --> M1, M2
# G2 --> M1, M2
# G3 --> M1, M3

# ForeignKey -- One Genre for a Movie -- One Parent for a Child

# single parent -- multiple child

# G1 --> M1
# G2 --> M2, M3

# ------------------------------------------------------------------------


# OneToOne
# ========

# single parent -- single child

# User - U1, U2, U3 -- Parent   Profile - P1, P2, P3

# U1 --> P1
# U2 --> P2

# ------------------------------------------------------------------------

# ManyToOne
# =========

# multiple parent -- single child

# Parent_Obj - A1, A2, A3   Child_Obj - B1, B2, B3

# A1, A2 --> B1/B2/B3
# A2, A3 --> B1/B2/B3

# ------------------------------------------------------------------------





class Comment(models.Model):

    message = models.CharField(max_length=200)

    owner = models.ForeignKey(User, on_delete=models.CASCADE) # one to many -- Foreign key

    post_object = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")

    # Comment.objects.filter(post_object=post_object) -- using child
    # post_object.post_comments.all() -- using parent

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): # for the string representation of an object

        return self.message






