from django.contrib import admin

from app.models import Product, Category, Cart, BuyHistory, Comment, Like

admin.site.register(Product),
admin.site.register(Category),
admin.site.register(Cart),
admin.site.register(Comment),
admin.site.register(BuyHistory),
admin.site.register(Like),

