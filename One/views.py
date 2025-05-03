from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from One.models import Category
from One.serializers import CustomUserRegistrationSerializer, DishSerializer


@api_view(['POST'])
def register(request):
    serializer = CustomUserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user=user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_menu(request):
    categories = Category.objects.all()
    data = []

    for category in categories:
        dishes = category.dishes.filter(is_active=True)
        serialized_dishes = DishSerializer(dishes, many=True).data
        data.append({
            'category': category.name,
            'dishes': serialized_dishes
        })
    return Response(data, status=status.HTTP_200_OK)
