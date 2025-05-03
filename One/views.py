from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from One.models import Category, Dish, CustomUser
from One.serializers import CustomUserRegistrationSerializer, DishSerializer, CategorySerializer


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serialized_categories = CategorySerializer(categories, many=True).data
    return Response(serialized_categories, status=status.HTTP_200_OK)

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
                'role': user.role,
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_menu(request,restaurant_id):
    restaurant = CustomUser.objects.get(id=restaurant_id)

    categories = Category.objects.all()
    data = []

    for category in categories:
        dishes = category.dishes.filter(is_active=True, restaurant=restaurant)
        serialized_dishes = DishSerializer(dishes, many=True).data
        data.append({
            'category': category.name,
            'dishes': serialized_dishes
        })

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_dishes_by_category(request,restaurant_id,category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"message":f"No category with id:{category_id}"},status=status.HTTP_404_NOT_FOUND)
    try:
        restaurant = CustomUser.objects.get(id=restaurant_id)
    except CustomUser.DoesNotExist:
        return Response({"message": f"No restaurant with id:{restaurant.id}"}, status=status.HTTP_404_NOT_FOUND)
    dishes = Dish.objects.filter(category=category, restaurant=restaurant)
    serialized_dishes = DishSerializer(dishes, many=True).data
    return Response(serialized_dishes, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_dish(request,dish_id):
    try:
        restaurant = request.user
    except CustomUser.DoesNotExist:
        return Response({"message": f"No restaurant with id:{restaurant.id}"}, status=status.HTTP_404_NOT_FOUND)
    try:
        dish = Dish.objects.get(id=dish_id)
    except Dish.DoesNotExist:
        return Response({"message": f"No dish with id:{dish_id}"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DishSerializer(dish).data
    return Response(serializer, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_dish(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"message":f"No category with id:{category_id}"},status=status.HTTP_404_NOT_FOUND)
    try:
        restaurant = request.user
        if restaurant.role != 'restaurant':
            return Response({"message": "You are not a restaurant"}, status=status.HTTP_403_FORBIDDEN)
    except CustomUser.DoesNotExist:
        return Response({"message": f"No restaurant with id:{restaurant.id}"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DishSerializer(data=request.data)
    if serializer.is_valid():
        dish = serializer.save(restaurant=request.user, category=category)
        dish.save()
        return Response(dish.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_dish(request,dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
        if dish.restaurant != request.user:
            return Response({"message":"You are not an owner"}, status=status.HTTP_403_FORBIDDEN)
    except Dish.DoesNotExist:
        return Response({"message": f"No dish with id:{dish_id}"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DishSerializer(dish, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dish(request,dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
        if dish.restaurant != request.user:
            return Response({"message":"You are not an owner"}, status=status.HTTP_403_FORBIDDEN)
    except Dish.DoesNotExist:
        return Response({"message": f"No dish with id:{dish_id}"}, status=status.HTTP_404_NOT_FOUND)
    dish.delete()
    return Response({"message":f"dish deleted id:{dish_id}"},status=status.HTTP_204_NO_CONTENT)