from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.serializers import Serializer
from .serializers import UserProfileSerializer, UserSerializer, UserUpdateSerializer,UserProfileUpdateSerializer
from .models import Account,UserProfile

class UserListView(APIView):

    def user_mapper(self, user):
        return {
            'id':user.user_id,
            'name':user.name,
            'username':user.user.username,
            'image':user.image.url
        }

    def get(self, request, *args, **kwargs):
        
        queryset = UserProfile.objects.select_related('user').all()
        searchquery = request.query_params.get('search')
        if(searchquery):
            filtered_qs = queryset.filter(Q(name__contains=searchquery) | Q(user__username__contains=searchquery))
            return Response(list(map(self.user_mapper,filtered_qs)))

        return Response(list(map(self.user_mapper,queryset)))

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

class LoggedUserView(APIView):

    def get_object(self, username):
        try:
            return Account.objects.get(username=username)
        except Account.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user = self.get_object(request.user)
        
        if not user:
            return Response({'username':'', 'name':''})

        profile = UserProfile.objects.get(user=user)

        userdata = {
            'id':user.id,
            'username':user.username,
            'name': profile.name,
            'image':profile.image.url
        }
        return Response(userdata)

class UserProfileView(APIView):

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,FormParser]

    def get(self, request, user_id, *args, **kwargs):

        user = Account.objects.get(id=user_id)
        userserializer = UserSerializer(user)
        
        userprofile = UserProfile.objects.get(user_id = user.id)

        serializer = UserProfileSerializer({
            'user':userserializer.data,
            'name':userprofile.name,
            'image':userprofile.image,
            'date_of_birth':userprofile.date_of_birth,
            'bio':userprofile.bio,
            'following_count':len(userprofile.following.all()),
            'followers_count': len(UserProfile.followers(userprofile))
            })
        
        return Response(serializer.data)

    def put(self, request,user_id, *args, **kwargs):
        
        user = Account.objects.get(id=user_id)
        profile = UserProfile.objects.get(user_id=user_id)

        userserializer = UserUpdateSerializer(user, data=request.data)
        profileserializer = UserProfileUpdateSerializer(profile, data = request.data)

        if userserializer.is_valid():
            if profileserializer.is_valid():
                userserializer.save()
                profileserializer.save()
                return Response({
                    **userserializer.data,
                    **profileserializer.data
                })

            return Response(profileserializer.errors)
        return Response(userserializer.errors)

class UserUpdateFollowView(APIView):

    def get(self,request, follower_id, user_id):
        user = UserProfile.objects.get(user_id=user_id)
        follower = UserProfile.objects.get(user_id=follower_id)
        return Response(follower.following.contains(user))

    def post(self,request, follower_id, user_id):

        user = UserProfile.objects.get(user_id=user_id)
        follower = UserProfile.objects.get(user_id=follower_id)

        if(follower.following.contains(user)):
            follower.following.remove(user)
        else:
            follower.following.add(user)

        account = Account.objects.get(id=user_id)
        userserializer = UserSerializer(account)
        
        userprofile = UserProfile.objects.get(user_id = account.id)

        serializer = UserProfileSerializer({
            'user':userserializer.data,
            'name':userprofile.name,
            'image':userprofile.image,
            'date_of_birth':userprofile.date_of_birth,
            'bio':userprofile.bio,
            'following_count':len(userprofile.following.all()),
            'followers_count': len(userprofile.followers())
            })

        return Response(serializer.data)

class UserFollowView(APIView):

    def user_mapper(self, user):
        return {
            'id':user.user_id,
            'name':user.name,
            'username':user.user.username,
            'image':user.image.url
        }


    def get(self, request,type, user_id):

        if(type=='followers'):
            userprofile = UserProfile.objects.get(user_id = user_id)

            followers = userprofile.followers().select_related('user').all()

            return Response(list(map(self.user_mapper,followers)))

        elif(type=='following'):
            following = UserProfile.objects.get(user_id = user_id).following.all()
            
            return Response(list(map(self.user_mapper,following)))
        
        return Response({'error':'url param type can only be followers or following'},status=status.HTTP_404_NOT_FOUND)
