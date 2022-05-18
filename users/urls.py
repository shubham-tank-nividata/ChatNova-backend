from django.urls import path,include
from .views import BlacklistTokenUpdateView,UserSignupView, UserProfileView, LoggedUserView, UserUpdateFollowView, UserFollowView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('loggeduser/',LoggedUserView.as_view()),
    path('profile/<int:user_id>',UserProfileView.as_view()),
    path('follow/<int:follower_id>/<int:user_id>/', UserUpdateFollowView.as_view()), #toggle user follow/unfollow
    path('<str:type>/<int:user_id>/', UserFollowView.as_view()), # type can be followers/following
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view()),
]