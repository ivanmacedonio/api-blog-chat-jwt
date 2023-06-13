from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PassSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 128, min_length = 6)
    password2 = serializers.CharField(max_length = 128, min_length = 6)

    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'password doesnt match!'})
        return data


class UserListSerializer(serializers.ModelSerializer): #solo serializa informacion para get's
    class Meta:
        model = User

        def to_representation(self,instance):
            return {
                'id':instance.id,
                'username':instance.username,
                'password':instance.password
            }
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class MesssageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'