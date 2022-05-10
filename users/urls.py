from django.urls import path,include
from .views import BlacklistTokenUpdateView

urlpatterns = [
    path('logout/blacklist', BlacklistTokenUpdateView.as_view()),
]