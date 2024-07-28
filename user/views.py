from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .utils import hash_user_password, verify_user_password
# Create your views here.

@api_view(['POST'])
def register_user(request):
    data = request.data
    email = data['email']
    name = data['name']
    mobile_phone = data['mobile_phone']
    password = data['password']
    #hash this password
    password = hash_user_password(password)
    user = User.objects.create(email=email, name=name, mobile_phone=mobile_phone, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    data = request.data
    email = data['email']
    password = data['password']
    #verify this password
    password = verify_user_password(password)
    user = User.objects.get(email=email, password=password)
    return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_users(request):
    user = User.objects.all()
    return Response({'data': user}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    return Response({'data': user}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request, user_id):
    data = request.data
    user = User.objects.get(id=user_id)
    user.email = data['email']
    user.name = data['name']
    user.mobile_phone = data['mobile_phone']
    user.password = data['password']
    user.save()
    return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
