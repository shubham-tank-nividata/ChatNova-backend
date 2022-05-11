from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer
from .models import Account,UserProfile

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSignupView(APIView):

    def post(self,request,*args, **kwargs):
        serializer = UserProfileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : f"Account Created Successfully for {serializer.data['name']}"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoggedUser(APIView):

    def get_object(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self.get_object(request.user)
        
        if not user:
            return Response({'username':'', 'name':''})

        userdata = {
            'username':user.username,
            'name': UserProfile.objects.get(user=user).name
        }
        return Response(userdata)