from django.shortcuts import render
from .models import *
from .serializers import *
from django.http.response import JsonResponse
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser


#----------------POSTS-------------------------------------

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = PostSerializer.Meta.model.objects.filter(state=True)


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self,request):
        return Post.objects.filter(user = request.user, state = True )
    

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(state=True)
    

#----------------PROFILE-------------------------------------

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = ProfileSerializer.Meta.model.objects.filter(state=True)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(state=True)
    

#----------------LOGIN/LOGOUT-------------------------------------

class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username = username, password = password)
        if user:
            token_serializer = self.serializer_class(data=request.data)
            if token_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': token_serializer.validated_data.get('access'),
                    'refresh': token_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesion exitoso!'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Usuario no valido!'}, status=status.HTTP_400_BAD_REQUEST)
        
class Logout(GenericAPIView):
    def post(self,request,*args,**kwargs):
            user = User.objects.filter(id=request.data.get('user',0))
            if user.exists():
                RefreshToken.for_user(user.first())
                return Response({'message': 'SESION CERRADA CORRECTAMENTE'}, status=status.HTTP_200_OK)
            return Response({'message': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)


#----------------USER-------------------------------------

class UserViewset(viewsets.GenericViewSet):
    serializer_class = CustomUserSerializer
    queryset = None

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True)
        return self.queryset
    
    def get_object(self,pk):
        return self.serializer_class().Meta.model.objects.filter(id=pk)
    
    @action(detail=True, methods=['post'])
    def change_password(self,request,pk=None):
        user = self.get_object(pk)
        password_serializer = PassSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({'message': 'Pass updated!'}, status=status.HTTP_200_OK)
        return Response({'password_error': 'Password validation error!'},status=status.HTTP_400_BAD_REQUEST)
    

    def list(self,request):
        users = self.get_queryset()
        serializer_classuser = UserListSerializer(users, many=True)
        return Response(serializer_classuser.data, status=status.HTTP_200_OK)
    
    def create(self,request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente! :)'}, status=status.HTTP_201_CREATED)
        return Response({'message_error': 'El usuario no pudo registrarse!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        user = self.get_object(pk)
        if user is not None:
            user_serializer = CustomUserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No se encontro el usuario!'},status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'Usuario no encontrado!'},status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk=None):
        user= self.get_object(pk)
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({'message': 'Usuario eliminado correctamente'},status=status.HTTP_200_OK)
        return Response({'error': 'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)
    

#----------------MENSAJERIA-------------------------------------  

class MessageViewSet(viewsets.GenericViewSet):
    serializer_class = MesssageSerializer
    queryset = None 

    def get_queryset(self, request,recibe):
        if self.queryset is None:
            return self.serializer_class().Model.objects.filter(envia = request.user, recibe = recibe)
        return self.queryset

    def list(self,request,recibe):
        messages = self.get_queryset()
        message_serializer  = self.serializer_class(messages, many = True)
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(message_serializer.data, status=status.HTTP_200_OK)

    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
    
    @action(detail=True, methods=('get'))
    def list_users(self,request):
        users = CustomUserSerializer.Meta.model.objects.exclude(username = request.user.username)
        serializer = UserListSerializer(users, many=True)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'error': 'No hay usuarios para listar'},status=status.HTTP_100_CONTINUE)
    
    @action(detail=True, methods=('get'))
    def message_view(request,self,recibe):
        messages = self.get_queryset()
        users = User.objects.exclude(username = request.user.username)
        receiver_1 = User.objects.filter(id=recibe).first()
        return Response({'users': users,
                         'receiver': recibe,
                         'messsages': messages}, status=status.HTTP_200_OK)
    
