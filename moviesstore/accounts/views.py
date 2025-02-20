from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm

def login(request):
    template_data = {'title': 'Login'}
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
        else:
            auth_login(request, user)
            return redirect('home.index')

    return render(request, 'accounts/login.html', {'template_data': template_data})

def signup(request):
    template_data = {'title': 'Sign Up'}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
    else:
        template_data['form'] = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

@login_required
def orders(request):
    template_data = {
        'title': 'Orders',
        'orders': request.user.order_set.all()
    }
    return render(request, 'accounts/orders.html', {'template_data': template_data})

# Custom password reset logic without email
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            request.session["reset_email"] = email  # Store email in session
            return redirect("password_reset_form")  # Redirect to custom reset form
        else:
            return render(request, "accounts/password_reset_form.html", {"error": "This email is not registered!"})

    return render(request, "accounts/password_reset_form.html")

def password_reset_form(request):
    template_data = {"title": "Reset Password"}

    email = request.session.get("reset_email")
    if not email:
        return redirect("password_reset")  # If session expired, restart process

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and confirm_password:
            if new_password == confirm_password:
                user = User.objects.filter(email=email).first()
                if user:
                    user.set_password(new_password)
                    user.save()
                    del request.session["reset_email"]  # Clear session
                    return redirect("accounts.login")  # Redirect to logi
                else:
                    template_data["error"] = "User not found."
            else:
                template_data["error"] = "Passwords do not match."
        else:
            template_data["error"] = "Please fill in all fields."

    return render(request, "accounts/password_reset_confirm.html", {"template_data": template_data})
