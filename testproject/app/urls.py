from django.urls import path
from app.views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/like/', like_product, name='product_like'),
    path('product/<slug:slug>/dislike/', dislike_product, name='product_dislike'),
    path('product/<slug:slug>/like-dislike/', like_dislike_product, name='product_like_dislike'),

    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('buy_confirm/', buy_confirm, name='buy_confirm'),
    path('buy_history/', BuyHistoryView.as_view(), name='buy_history'),

    path('add_to_cart/<slug:slug>/', add_product, name='add_to_cart'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]