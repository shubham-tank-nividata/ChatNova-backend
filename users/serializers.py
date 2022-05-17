from rest_framework import serializers
from users.models import Account
from .models import UserProfile
from datetime import date
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        return make_password(value)

    class Meta:
        model = Account
        fields = ('username', 'email','password' )


class UserProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ('user','name','date_of_birth','image','bio')

    def create(self,validated_data):

        user = UserSerializer.create(UserSerializer(), validated_data=validated_data.get('user'))
        profile = UserProfile.objects.create(
                            user=user,
                            name=validated_data.get('name'),
                            date_of_birth= validated_data.get('date_of_birth'),
                            bio=validated_data.get('bio'),
                        )
        return profile

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'email','password' )

class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name','date_of_birth','image','bio')