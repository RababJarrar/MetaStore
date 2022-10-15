from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt


class User_Manager(models.Manager):
    def validate_user(self, request_data):
        errors = {}
        email = request_data.POST.get('email')
        users = Customer.objects.filter(email=email)
        if len(request_data.POST.get('first_name')) < 2:
            errors['first_name'] = 'username should be at least 2 letters'
        if len(request_data.POST.get('last_name')) < 2:
            errors['last_name'] = 'lastname should be at least 2 letters'
        if len(request_data.POST['password']) < 8:
            errors["password"] = "The Password should be at least 8 characters"
        if request_data.POST['password'] != request_data.POST.get('confirm_password') and request_data.POST.get('confirm_password'):
            errors['password'] = 'password does not match'
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if len(users) > 0:
            errors['user_exist'] = 'User with this email already exist!'

        return errors

    def validate_seller(self, request_data):
        errors = {}
        email = request_data.POST.get('email')
        users = Seller.objects.filter(email=email)
        if len(request_data.POST.get('seller_name')) < 2:
            errors['seller_name'] = 'name should be at least 2 letters'
        if len(request_data.POST['password']) < 8:
            errors["password"] = "The Password should be at least 8 characters"
        if request_data.POST['password'] != request_data.POST.get('confirm_password') and request_data.POST.get('confirm_password'):
            errors['password'] = 'password does not match'
        EMAIL_REGEX = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if len(users) > 0:
            errors['user_exist'] = 'User with this email already exist!'

        return errors

    def validate_login(self, request_date):
        errors = {}
        email = request_date.POST.get('email')
        password = request_date.POST.get('password')
        user = Customer.objects.filter(email=email)
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if user:
            if bcrypt.checkpw(password.encode(), user[0].password.encode()) == False:
                errors['password'] = 'username or password does not match'
        if not user:
            errors['user_email'] = 'User with this email doesn\'t exist'
        return errors

    def validate_login_seller(self, request_date):
        errors = {}
        email = request_date.POST.get('email')
        password = request_date.POST.get('password')
        user = Seller.objects.filter(email=email)
        EMAIL_REGEX = re.compile(
            '^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email format"
        if user:
            if bcrypt.checkpw(password.encode(), user[0].password.encode()) == False:
                errors['password'] = 'username or password does not match'
        if not user:
            errors['user_email'] = 'User with this email doesn\'t exist'
        return errors


class Customer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=95)
    mobile = models.IntegerField()
    address = models.TextField()
    objects = User_Manager()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)


class Seller(models.Model):
    name = models.CharField(max_length=55)
    mobile = models.IntegerField()
    email = models.CharField(max_length=95)
    picture = models.ImageField(upload_to='media/', null=True, blank=True)
    description = models.TextField()
    city = models.CharField(max_length=55)
    password = models.CharField(max_length=80)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = User_Manager()
