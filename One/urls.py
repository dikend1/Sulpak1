from django.urls import path
from . import views
from One import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('menu/<int:restaurant_id>', views.get_menu, name='get_menu'),
    path('menu/categories/',views.get_categories,name='get_categories'),
    path('menu/<int:restaurant_id>/<int:category_id>/get_dishes/', views.get_dishes_by_category, name='get_dishes_by_category'),

    path('menu/<int:dish_id>/', views.get_dish, name='get_dish'),

    path('menu/<int:category_id>/add_dish/', views.add_dish , name="add_dish"),
    path('menu/<int:dish_id>/edit_dish/', views.edit_dish, name='edit_dish',),
    path('menu/<int:dish_id>/delete_dish/', views.delete_dish, name='delete_dish'),
]