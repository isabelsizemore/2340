from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('signup/', views.signup, name='accounts.signup'),

    # Custom password reset flow
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password_reset_form/", views.password_reset_form, name="password_reset_form"),
    path('orders/', views.orders, name='accounts.orders'),
]
