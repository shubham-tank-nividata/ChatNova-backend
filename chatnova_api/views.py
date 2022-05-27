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
            post = Post.objects.get(id=serializer.data.get('id'))

            return Response({
                'id':post.id,
                'user_id':post.user.id,
                'name':post.user.userprofile.name,
                'username':post.user.username,
                'profile_image':post.user.userprofile.image.url,
                'content':post.content,
                'image':post.image.url if post.image else None,
                'created_at':post.created_at,
            })
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

class PostRetriveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListCreateView(APIView):

    def user_mapper(self, comment):
        return {
            'id':comment.id,
            'user_id':comment.user_id,
            'name':comment.user.userprofile.name,
            'username':comment.user.username,
            'image':comment.user.userprofile.image.url,
            'comment_text':comment.comment_text,
            'created_at':comment.created_at,
        }

    def get(self, request,post_id,*args, **kwargs):

        comments = Comment.objects.filter(post = post_id).select_related('user').order_by('created_at').all()

        return Response(list(map(self.user_mapper,comments)))

    def post(self, request, post_id, *args, **kwargs):
        comment = Comment(user_id=request.data['user_id'], post_id=post_id, comment_text=request.data['comment_text'])
        comment.save()
        return Response({'id':comment.id, 'user_id':comment.user_id, 'post_id':comment.post_id, 'comment_text':comment.comment_text})


class CommentRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id).all()
    
    serializer_class = CommentSerializer


class LikeList(APIView):

    def user_mapper(self, like):
        return {
            'id':like.user_id,
            'name':like.user.userprofile.name,
            'username':like.user.username,
            'image':like.user.userprofile.image.url
        }

    def get(self, request,post_id,*args, **kwargs):

        likes = Like.objects.filter(post = post_id).select_related('user').all()

        return Response(list(map(self.user_mapper,likes)))

class LikeCreateRetriveDeleteView(APIView):

    def get(self, request, user_id, post_id,*args, **kwargs):
        isLiked = Like.objects.filter(post_id=post_id, user_id=user_id).exists()
        return Response(isLiked)

    def post(self, request, user_id, post_id, *args, **kwargs):
        like = Like.objects.filter(user_id=user_id, post_id=post_id)
        if like.count() != 0:
            like = like.first()
            return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })
        
        like = Like(user_id=user_id, post_id=post_id)
        like.save()
        return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })
    
    def delete(self, request, user_id, post_id, *args, **kwargs):
        like = Like.objects.filter(user_id=user_id,post_id=post_id)
        if like.count() == 0:
            like = like.first()
            return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })
        like = like.first()
        like.delete()
        return Response({'id':like.id, 'user_id':user_id, 'post_id': post_id })

