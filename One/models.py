from django.db import models

# Тамак ушын мысалы салат Основные блюда
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='Category')

    def __str__(self):
        return self.name

# Блюда
class Dish(models.Model):
    name = models.CharField(max_length=200,verbose_name='Dish')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Price')
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE,verbose_name='Category')
    image = models.ImageField(uplaod_to='images/',null = True,blank=True,verbose_name='Image')

    def __str__(self):
        return self.name


#Заказы
class Order(models.Model):
    user_name = models.CharField(max_length=100,verbose_name='Name_client')
    dishes = models.CharField(Dish, related_name='orders', verbose_name='Dish')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Total_price')
    created_at = models.DateField(auto_now_add=True,verbose_name='Created_at')
    status = models.CharField(max_length=50,choices=[('pending')])