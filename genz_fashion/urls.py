from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('contact',contact,name='contact'),
    path('product_detail/<int:id>',product_detail,name='product_detail'),
    path('checkout',checkout,name='chreckout'),
    path('shop',shop,name='shop'),
    path('cart',cart,name='cart'),
    path('signup',signup,name='signup'),
    path('login_user',login_user,name='login_user'),
    path('logout_view',logout_view,name='logout_view'),
]
