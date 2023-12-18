from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f'{self.user.username} - {self.content_type}'

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f'{self.user.username} - {self.content_type}'


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    slug = models.SlugField(max_length=255, blank=True)
    likes = GenericRelation(Like)
    dislikes = GenericRelation(Dislike)

    def __str__(self):
        return f"{self.title} - {self.price}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(f'{self.title} - {self.price}')
        return super(Product, self).save()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_list = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username


class BuyHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product_list = models.ManyToManyField(Product)
    buy_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    publish = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f'{self.user.username} \n {self.body}'


