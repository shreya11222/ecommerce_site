from django.urls import path, include
from . import views


urlpatterns = [
    path('about/', views.about_view, name='about'),

    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_detail, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('admin/products/add/', views.admin_product_add, name='admin_product_add'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/products/add/', views.product_add, name='product_add'),
    path('admin/products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('admin/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('contact/', views.contact, name='contact'),
     path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.place_order, name='place_order'),
        path('', views.home, name='home'),  # Home page
    path('products/', views.product_list, name='product_list'),  # Products listing
    path('products/<int:pk>/', views.product_detail, name='product_detail'), 
]
