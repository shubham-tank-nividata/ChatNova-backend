from django.urls import path,include
from .views import BlacklistTokenUpdateView,UserSignupView, UserProfileView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('profile/<int:user_id>',UserProfileView.as_view()),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view()),
]