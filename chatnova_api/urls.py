from django.urls import path,include
from .views import PostDetail,CommentList, LikeList, UserPostListCreateView, followingPostList, LikeCreateRetriveDeleteView

app_name='chatnova_api'

urlpatterns = [
    path('users/<int:user_id>/posts', UserPostListCreateView.as_view(), name='user-post-list'),
    path('following/posts', followingPostList.as_view(),name='following-post-list'),
    path('posts/<int:pk>',PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments',CommentList.as_view(), name='comment-list'),
    path('posts/<int:post_id>/likes',LikeList.as_view(), name='like-list'),
    path('users/<int:user_id>/likes/<int:post_id>', LikeCreateRetriveDeleteView.as_view())
]