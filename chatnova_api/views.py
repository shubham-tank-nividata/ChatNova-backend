from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from users.models import Account, UserProfile

class UserPostListCreateView(APIView):

    def user_post(self, post):
        return {
            'id':post.id,
            'user_id':post.user.id,
            'name':post.user.userprofile.name,
            'username':post.user.username,
            'profile_image':post.user.userprofile.image.url,
            'content':post.content,
            'image':post.image.url if post.image else None,
            'created_at':post.created_at,
        }

    def get(self, request, user_id,*args, **kwargs):
        user = Account.objects.get(id=user_id)
        posts = list(user.post_set.order_by('-created_at'))
        return Response(list(map(self.user_post,posts)))

    def post(self, request, user_id,*args, **kwargs):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class followingPostList(APIView):

    def user_post(self, user,post):
        return {
            'id':post.id,
            'user_id':user.user_id,
            'name':user.name,
            'username':user.user.username,
            'profile_image':user.image.url,
            'content':post.content,
            'image':post.image.url if post.image else None,
            'created_at':post.created_at,
            'likes_count' : post.like_set.count(),
            'comments_count' : post.comment_set.count()
        }
    
    def get(self, request):
        # followings = UserProfile.objects.get(user=request.user).following.all()
        user_id = request.user.id
        followings = UserProfile.objects.get(user=user_id).following.all()


        users = (followings | UserProfile.objects.filter(user=user_id)).distinct()

        posts = []

        for user in users:
            for post in user.user.post_set.all():
                posts.append(self.user_post(user,post))

        return Response(sorted(posts, key=lambda post: post['created_at'], reverse=True))

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentList(APIView):

    def get(self, request,post_id,*args, **kwargs):
        comments = Comment.objects.filter(post = post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class LikeList(APIView):

    def get(self, request,post_id,*args, **kwargs):
        likes = Like.objects.filter(post = post_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class LikeCreateRetriveDeleteView(APIView):

    def get(self, request, user_id, post_id,*args, **kwargs):
        isLiked = Like.objects.filter(post_id=post_id, user_id=user_id).exists()
        return Response(isLiked)

    def post(self, request, user_id, post_id, *args, **kwargs):
        like = Like(user_id=user_id, post_id=post_id)
        like.save()
        return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })
    
    def delete(self, request, user_id, post_id, *args, **kwargs):
        like = Like.objects.get(user_id=user_id,post_id=post_id)
        like.delete()
        return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })

