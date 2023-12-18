from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, FormView, DetailView

from app.forms import CommentModelForm
from app.models import Product, Cart, BuyHistory, Comment, Like, Dislike


class ProductListView(ListView):
    template_name = 'app/product_list.html'
    model = Product


class RegisterUser(CreateView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('product_list')

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST.get('username'))
            Cart.objects.create(user=user)
            return redirect('product_list')
        else:
            return redirect('register')


class UserLoginView(LoginView):
    template_name = 'app/login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('product_list')


def logout_user(request):
    logout(request)
    return redirect('product_list')


class ProfileView(ListView):
    template_name = 'app/profile.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        print(cart.product_list.all())
        return cart.product_list.all()


def add_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    Cart.objects.get(user=request.user).product_list.add(product)
    return redirect('product_list')


def buy_confirm(request):
    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.get(user=user)

        bh = BuyHistory.objects.create(user=user)
        bh.product_list.set(cart.product_list.all())
        cart.product_list.clear()

        return redirect('cart')


class CartView(ListView):
    template_name = 'app/cart.html'

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user).product_list.all()

class BuyHistoryView(ListView):
    template_name = 'app/buy_history.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        return BuyHistory.objects.filter(user=self.request.user)


class ProductDetailView(DetailView, FormView):
    template_name = 'app/product_detail.html'
    form_class = CommentModelForm
    model = Product

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(request.POST)
        slug = request.path.split('/')[-2]
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                product=Product.objects.get(slug=slug),
                body=form.cleaned_data['body']
            )
            return redirect('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(product=self.object)
        return context


def like_product(request, slug):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(Product, slug=slug)
        like = Like.objects.create(content_object=product, user=user)
        like.save()
        return redirect('product_list')


def dislike_product(request, slug):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(Product, slug=slug)
        # Create or get existing dislike object
        dislike, _ = Dislike.objects.get_or_create(content_object=product, user=user)
        # Check if already disliked
        if dislike.active:
            dislike.active = False
            dislike.save()
            message = f'You un-disliked "{product.name}".'
        else:
            dislike.active = True
            dislike.save()
            message = f'You disliked "{product.name}".'

        # Redirect with a success message
        request.session['message'] = message
        return redirect('product_list')
    return redirect('product_list')


def like_dislike_product(request, slug):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(Product, slug=slug)

        # Check if user has already liked or disliked
        like = Like.objects.filter(content_object=product, user=user).first()
        dislike = Dislike.objects.filter(content_object=product, user=user).first()

        # Handle different actions based on existing likes/dislikes
        if like:
            like.delete()
            message = f'You unliked "{product.name}".'
        elif dislike:
            dislike.active = not dislike.active
            dislike.save()
            message = f'{"Un" if dislike.active else "Dis"}liked "{product.name}".'
        else:
            Like.objects.create(content_object=product, user=user)
            message = f'You liked "{product.name}".'

        # Set and display message using session
        request.session['message'] = message
        return redirect('product_list')
    return redirect('product_list')