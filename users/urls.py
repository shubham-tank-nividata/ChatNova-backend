from django.urls import path,include
from .views import BlacklistTokenUpdateView,UserSignup

urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view()),
]