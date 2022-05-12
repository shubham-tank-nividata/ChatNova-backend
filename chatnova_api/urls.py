from django.urls import path,include
from .views import PostDetail,CommentList, LikeList

app_name='chatnova_api'

urlpatterns = [
    path('posts/<int:pk>',PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments',CommentList.as_view(), name='comment-list'),
    path('posts/<int:post_id>/likes',LikeList.as_view(), name='like-list'),
]