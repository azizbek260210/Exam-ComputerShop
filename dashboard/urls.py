from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Index and Auth
    path('', views.index, name='index'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:id>/', views.category_update, name='category_update'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),

    # Enter Product URLs
    path('enter-products/', views.enter_product_list, name='enter_product_list'),
    path('enter-products/create/', views.create_enter_product, name='create_enter_product'),
    path('enter-products/<int:id>/', views.enter_product_detail, name='enter_product_detail'),

    # Sell Product URLs
    path('sell-products/', views.sell_product_list, name='sell_product_list'),
    path('sell-products/create/', views.sell_product_create, name='sell_product_create'),
    path('sell-products/update/<int:id>/', views.sell_product_update, name='sell_product_update'),
    path('sell-products/<int:id>/', views.sell_product_detail, name='sell_product_detail'),

    # Refund URLs
    path('refunds/', views.refund_list, name='refund_list'),
    path('refunds/<int:id>/', views.refund_detail, name='refund_detail'),
    path('refund/<int:id>/', views.refund, name='refund'),

    # Filter URLs
    path('filter/', views.filter, name='filter'),
    path('filter/entries/', views.filter_entries, name='filter_entries'),
]

