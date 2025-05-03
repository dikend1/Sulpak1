from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('restaurant', 'Restaurant'),
        ('customer', 'Customer'),
    )
    email = models.EmailField(unique=True, null=True, blank=True)

    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=11, choices=ROLE_CHOICES)

    qr_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'username']

    def __str__(self):
        return f"{self.email} - {self.role}"


# Тамак ушын мысалы салат Основные блюда
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Блюда
class Dish(models.Model):
    restaurant = models.ForeignKey(CustomUser, related_name='dishes', on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    image = models.URLField(blank=True,null=True,default="")
    is_active = models.BooleanField(default=True)
    ingredients = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dish = models.ForeignKey(Dish, related_name='reviews', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # Оценка блюда
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв на {self.dish.name} от {self.user_name}"



class Order(models.Model):
    customer = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE, verbose_name="Заказчик")
    dishes = models.ManyToManyField(Dish, related_name='orders')
    total_price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    user_number = models.CharField(max_length=12)
    order_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'В ожидании'), ('Completed', 'Завершен'), ('Cancelled', 'Отменен')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.id} от {self.user_name}"


class DeliveryStatus(models.Model):
    order = models.ForeignKey(Order, related_name='delivery_statuses', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Preparing', 'Готовится'), ('Dispatched', 'Отправлено'), ('Delivered', 'Доставлено')])
    timestamp = models.DateTimeField(auto_now_add=True)  # Время изменения статуса

    def __str__(self):
        return f"Статус доставки для заказа {self.order.id}: {self.status}"


