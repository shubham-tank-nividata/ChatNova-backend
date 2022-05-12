from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentList(APIView):

    def get(self, request,post_id,*args, **kwargs):
        comments = Comment.objects.filter(post = post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class LikeList(APIView):

    def get(self, request,post,*args, **kwargs):
        likes = Like.objects.filter(post = post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)