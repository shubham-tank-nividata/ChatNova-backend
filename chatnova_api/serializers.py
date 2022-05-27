from rest_framework import serializers
from .models import Post, Like, Comment
from users.models import Account


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user',)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id','post','user', 'comment_text', 'created_at',)

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id','user', 'content','image','created_at','like_set','comment_set',)