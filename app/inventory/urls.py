from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import DashboardView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    
    path('inventory/', views.ingredient_list, name='ingredient_list'),
    path('inventory/delete/<int:pk>/', views.ingredient_delete, name='ingredient_delete'),
    path('inventory/update/<int:pk>/', views.ingredient_update, name='ingredient_update'),
    path('inventory/add/', views.ingredient_add, name='ingredient_add'),

    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.menu_add, name='menu_add'),
    path('menu/<int:menu_item_id>/add-requirements/', views.add_requirements, name='add_requirements'),

    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/add/', views.purchase_add, name='purchase_add'),

    path('report/', views.report, name='report'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
