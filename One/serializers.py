from rest_framework import serializers
from .models import CustomUser, Dish, Category, Order, Review


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password','username','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
                role=validated_data['role']
        )
        return user

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'image', 'ingredients']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','address','role']

class OrderCreateSerializer(serializers.ModelSerializer):
    dishes = serializers.ListField(child=serializers.IntegerField())  # Список ID блюд

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'customer', 'dishes', 'total_price', 'user_number', 'order_status']

    def create(self, validated_data):
        # Извлекаем блюда из данных и убираем их из валидированных данных
        dishes_data = validated_data.pop('dishes', [])
        order = super().create(validated_data)

        # Добавляем блюда в заказ
        for dish_id in dishes_data:
            dish = Dish.objects.get(id=dish_id)
            order.dishes.add(dish)

        return order

class OrderSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True,read_only=True)
    customer = CustomerSerializer()
    class Meta:
        model = Order
        fields = ['id','restaurant','customer', 'dishes', 'total_price','created_at','user_number','order_status']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','rating','review_text','restaurant']

class RestaurantSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'address', 'role', 'dop_info', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 2)
        return 1