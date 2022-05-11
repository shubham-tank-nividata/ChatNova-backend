from django.urls import path,include
from .views import BlacklistTokenUpdateView,UserSignupView, LoggedUser

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('loggeduser/',LoggedUser.as_view()),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view()),
]