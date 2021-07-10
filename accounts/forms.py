from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import Customer, Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user"]
