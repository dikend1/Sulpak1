import uuid
import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from One.models import Category, Dish, CustomUser, Order
from One.serializers import CustomUserRegistrationSerializer, DishSerializer, CategorySerializer, OrderSerializer,OrderCreateSerializer
from Sulpak1 import settings

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
    print(restaurant_id)
    if restaurant.role != 'restaurant':
        return Response({"message":"id belongs to not the restaurant"}, status=status.HTTP_403_FORBIDDEN)

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
@parser_classes([MultiPartParser])
def add_dish(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"message": f"No category with id:{category_id}"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user.role != 'restaurant':
        return Response({"message": "You are not a restaurant"}, status=status.HTTP_403_FORBIDDEN)

    image_file = request.FILES.get('image')
    image_url = ""

    if image_file:
        extension = image_file.name.split('.')[-1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        path = f"dish_photos/{filename}"

        content_type = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp'
        }.get(extension, 'application/octet-stream')

        SUPABASE_URL = settings.SUPABASE_URL.rstrip('/')
        bucket = settings.STORAGE_BUCKET_NAME
        service_key = settings.SERVICE_ROLE_KEY

        upload_url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{path}"
        headers = {
            "Authorization": f"Bearer {service_key}",
            "Content-Type": content_type,
            "x-upsert": "true"
        }

        response = requests.put(upload_url, headers=headers, data=image_file.read())

        if response.status_code == 200:
            image_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}"
        else:
            return Response({"error": f"Image upload failed: {response.status_code}"}, status=500)

    # Вставляем image_url вручную
    data = request.data.copy()
    data['image'] = image_url

    serializer = DishSerializer(data=data)
    if serializer.is_valid():
        dish = serializer.save(restaurant=user, category=category)
        return Response(DishSerializer(dish).data, status=status.HTTP_201_CREATED)
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

@api_view(['POST'])
def add_order(request):
    data = request.data
    # Создаем сериализатор с переданными данными
    serializer = OrderCreateSerializer(data=data)

    if serializer.is_valid():
        # Сохраняем заказ (создается новый заказ)
        order = serializer.save(customer=request.user, restaurant=data.get('restaurant'))

        # Добавляем блюда в заказ (Many-to-Many связь)
        dishes = data.get('dishes', [])
        for dish_id in dishes:
            try:
                dish = Dish.objects.get(id=dish_id)  # Получаем блюдо по id
                order.dishes.add(dish)  # Добавляем блюдо в заказ
            except Dish.DoesNotExist:
                return Response({"detail": f"Dish with id {dish_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем заказ
        order.save()

        # Возвращаем ответ с сериализованными данными заказа
        return Response(OrderCreateSerializer(order).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_orders_id(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({
            "detail": "Order not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_customer_orders(request, customer_id):
    try:
        customer = CustomUser.objects.get(id=customer_id)
        if customer.role != 'customer' or customer.role != 'Customer':
            return Response({"message": "you are not customer"}, status=status.HTTP_403_FORBIDDEN)
        orders = Order.objects.filter(customer=customer)
        if not orders:
            return Response({"detail": "No orders found for this customer."}, status=status.HTTP_404_NOT_FOUND
                            )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "detail": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_restaurant_orders(request, restaurant_id):
    try:
        restaurant = CustomUser.objects.get(id=restaurant_id)
        if restaurant.role != 'restaurant' or restaurant.role != 'Restaurant':
            return Response({"message": "you are not rest"}, status=status.HTTP_403_FORBIDDEN)

        orders = Order.objects.filter(restaurant=restaurant)

        if not orders:
            return Response({"detail": "No orders found for this restaurant."}, status=status.HTTP_404_NOT_FOUND
                            )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "detail": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)