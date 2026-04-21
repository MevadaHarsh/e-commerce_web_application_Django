from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings    

# Create your views here.
def index(request):
    category=Category.objects.all()
    context={
        'category':category,
    }
    return render(request,'index.html', context)

def cart(request):
    return render(request,'cart.html')

def contact(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']

        created=ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        send_mail(
            subject="Team GENZ FASHION",
            message="Thank you for your email. our team will gt back to you soon.",
            recipient_list=[email],
            from_email= settings.EMAIL_HOST_USER,
            fail_silently=False
        )
        
        send_mail(
            subject,
            message,
            recipient_list=[settings.EMAIL_HOST_USER],
            from_email= settings.EMAIL_HOST_USER,
            fail_silently=False
        )
        created.save()
        
    return render(request,'contact.html')

def product_detail(request,id):
    category=Category.objects.get(id=id)
    product=Product.objects.filter(category=category)
    context={
        "category":category,
        "product":product
    }
    return render(request,'detail.html', context)

def checkout(request):
    return render(request,'checkout.html')

def shop(request):
    return render(request,'shop.html')

def signup(request):
    if request.method == 'POST' :
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        
        created=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
        )
        created.set_password(password)
        created.save()
        
    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        if not any([username, password]):
            messages.error(request, 'Please enter your username and password')
            return render(request, 'login.html')
        user=authenticate(request,username=username, password=password)
        
        if not user:
            messages.error(request,'Invalid username or password')
            return render(request, 'login.html')
        login(request,user)
        messages.success(request,'You have been logged in')
        return redirect('index')
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('index')

def cart(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('login')
    cart,created=Cart.objects.get_or_create(user=user)
    cart_item=cart.items.all()
    subtotal=0
    for item in cart_item:
        subtotal+= item.total_price()

    context={
        'cart_items':cart_item,
        'subtotal' : subtotal 
    }
    
    created.save()
    return render(request, 'cart.html', context)

def add_to_cart(request,id):
    user=request.user
    if not user.is_authenticated:
        return redirect('login')

    product=Product.objects.get(id=id)
    cart=Cart.objects.get_or_create(user=user)[0]
    cart_item=CartItem.objects.get_or_create(Cart=cart, Product=product)[0]
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')