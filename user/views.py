from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .utils import hash_user_password, verify_user_password
from django.http import JsonResponse

# Create your views here.

@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        email = data['email']
        username = data['username']
        mobile_phone = data['mobile_phone']
        password = data['password']
        balance = data.get('balance', 0.0)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already in use'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(mobile_phone=mobile_phone).exists():
            return Response({'message': 'Mobile phone already in use'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password
        password = hash_user_password(password)
        user = User.objects.create(email=email, username=username, mobile_phone=mobile_phone, password=password, balance=balance)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    try:
        data = request.data
        email = data['email']
        password = data['password']
        user = User.objects.all()
        user = User.objects.get(email=email)
        #password = hash_user_password(password)
        print(password)
        print(user.password)
        if not verify_user_password(password, user.password):
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_users(request):
    try:
        users = User.objects.all()
        user_list = []
        for user in users:
            user_dict = {
                'user_id': user.user_id,
                'email': user.email,
                'username': user.username,
                'mobile_phone': user.mobile_phone,
                'balance': user.balance,
            }
            user_list.append(user_dict)
        
        return JsonResponse(user_list, safe=False)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user(request, username):
    try:
        user = User.objects.get(username=username)
        return Response({'data': {
            'user_id': user.user_id,
            'email': user.email,
            'username': user.username,
            'mobile_phone': user.mobile_phone,
            'balance': user.balance,
        }}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_user(request, username):
    try:
        data = request.data
        user = User.objects.get(username=username)
        user.email = data['email']
        user.username = data['username']
        user.mobile_phone = data['mobile_phone']
        user.password = hash_user_password(data['password']) # Hash the updated password
        user.balance = data.get('balance', user.balance)
        user.save()
        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_user(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
