from os import name
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    # Login- register -logout
    path("register/", views.RegisterPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    # user page and account page
    path("account/", views.account_page, name="account"),
    path("user/", views.userPage, name="user-page"),
    # dashboard admin pages
    path("customer/<str:pk>/", views.customer, name="customer"),
    path("createcustomer/", views.CreateCustomer, name="CreateCustomer"),
    path("products/", views.products, name="products"),
    path("create_order/<str:pk>", views.create_order, name="create_order"),
    path("update_form/<str:pk>", views.update_form, name="update_form"),
    path("delete_order/<str:pk>", views.delete_order, name="delete_order"),
    # Password reset
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
