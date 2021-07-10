from django.contrib import auth
from django.forms.formsets import all_valid
from django.shortcuts import redirect, render
from .models import *
from .forms import CreateCustomerForm, CreateUserForm, OrderForm, CustomerForm
from django.forms import inlineformset_factory

from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import admin_only, unauthenticated_user, allowed_users

# Create your views here.


@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_pending = orders.filter(status="Pending").count()
    total_orders = orders.count()
    total_delivered = orders.filter(status="Delivered").count()

    context = {
        "orders": orders,
        "customers": customers,
        "total_pending": total_pending,
        "total_orders": total_orders,
        "total_delivered": total_delivered,
        "total_customers": total_customers,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def products(request):
    products = Products.objects.all()
    return render(request, "accounts/products.html", {"products": products})


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        "customer": customer,
        "orders": orders,
        "orders_count": orders_count,
        "myFilter": myFilter,
    }
    return render(request, "accounts/customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def create_order(request, pk):

    order_form_set = inlineformset_factory(
        Customer, Order, fields=("product", "status")
    )
    customer = Customer.objects.get(id=pk)
    formset = order_form_set(instance=customer)
    # form = OrderForm(initial={"customer": customer})
    if request.method == "POST":
        # print("Print", request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"formset": formset}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def update_form(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        # print("Print", request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}
    return render(request, "accounts/update_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"item": order}
    return render(request, "accounts/delete.html", context)


@login_required(login_url="login")
def CreateCustomer(request):
    form = CreateCustomerForm()
    if request.method == "POST":
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}

    return render(request, "accounts/createcustomer.html", context)


@allowed_users(allowed_roles=["customer"])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_pending = orders.filter(status="Pending").count()
    total_orders = orders.count()
    total_delivered = orders.filter(status="Delivered").count()

    print("ORDERES:", orders)
    context = {
        "orders": orders,
        "total_pending": total_pending,
        "total_orders": total_orders,
        "total_delivered": total_delivered,
    }
    return render(request, "accounts/user.html", context)


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username OR password incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@unauthenticated_user
def RegisterPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + username)

            return redirect("login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


# @unauthenticated_user
# @allowed_users(allowed_roles=['customer'])
def account_page(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = {"form": form}

    return render(request, "accounts/account.html", context)


