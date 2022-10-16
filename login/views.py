from django.shortcuts import render, redirect
from django.contrib import messages
from storeapp.models import Customer, Seller
import bcrypt
# Create your views here.


def index(request):
    return redirect('/store')


def view_customer_login(request):
    return render(request, 'login/login.html')


def login_customer(request):
    request.session.clear()
    request.session.modified = True
    errors = Customer.objects.validate_login(request)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        email = request.POST.get('email')
        customer = Customer.objects.get(email=email)
        request.session['customer_id'] = customer.id
        request.session.modified = True
        return redirect('/store')


def create_customer(request):
    request.session.clear()
    request.session.modified = True
    errors = Customer.objects.validate_user(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            address=address,
            password=password_hash
        )
        customer.save()
        request.session['customer_id'] = customer.id
        request.session.modified = True
        return redirect('/store')


def view_seller_login(request):

    return render(request, 'login/seller_signup.html')


def login_seller(request):
    request.session.clear()
    request.session.modified = True
    errors = Seller.objects.validate_login_seller(request)
    if len(errors) > 0:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_seller_view')
    else:
        email = request.POST.get('email')
        seller = Seller.objects.get(email=email)
        request.session['seller_id'] = seller.id
        request.session.modified = True

        return redirect('/store/seller')


def create_seller(request):
    request.session.clear()
    request.session.modified = True
    errors = Seller.objects.validate_seller(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login_seller_view')
    seller_name = request.POST.get('seller_name')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    description = request.POST.get('description')
    city = request.POST.get('city')
    password = request.POST.get('password')
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_seller = Seller.objects.create(
        name=seller_name,
        mobile=mobile,
        email=email,
        description=description,
        city=city,
        password=password_hash
    )
    new_seller.save()
    request.session['seller_id'] = new_seller.id
    request.session.modified = True
    return redirect('/store/seller')
