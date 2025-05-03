from django.contrib.auth.models import AbstractUser
from django.db import models


class Restaurant(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    qr_url = models.URLField(blank=True,null=True,default="")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password','email']

    def __str__(self):
        return self.email

# Тамак ушын мысалы салат Основные блюда
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Блюда
class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    image = models.URLField(blank=True,null=True,default="")

    def __str__(self):
        return self.name


#Заказы
class Order(models.Model):
    user_name = models.CharField(max_length=100)
    dishes = models.ManyToManyField(Dish, related_name='orders')
    total_price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    number = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.id} от {self.user_name}"

class Review(models.Model):
    dish = models.ForeignKey(Dish, related_name='reviews', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # Оценка блюда
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв на {self.dish.name} от {self.user_name}"


class DeliveryStatus(models.Model):
    order = models.ForeignKey(Order, related_name='delivery_statuses', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Preparing', 'Готовится'), ('Dispatched', 'Отправлено'), ('Delivered', 'Доставлено')])
    timestamp = models.DateTimeField(auto_now_add=True)  # Время изменения статуса

    def __str__(self):
        return f"Статус доставки для заказа {self.order.id}: {self.status}"


