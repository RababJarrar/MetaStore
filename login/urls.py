from django.urls import path
from login import views
urlpatterns = [
    path('', views.view_customer_login),
    path('login_customer', views.login_customer),
    path('signup_customer', views.create_customer),
    path('login_seller_view', views.view_seller_login),
    path('seller_login', views.login_seller),
    path('seller_signup', views.create_seller),
]
