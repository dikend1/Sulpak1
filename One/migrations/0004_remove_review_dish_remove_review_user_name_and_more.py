# Generated by Django 5.2 on 2025-05-03 22:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('One', '0003_order_restaurant_alter_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='dish',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user_name',
        ),
        migrations.AddField(
            model_name='review',
            name='customer',
            field=models.ManyToManyField(default='', related_name='customer_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='restaurant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
