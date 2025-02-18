from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = CustomUserCreationForm()
    if request.method == 'GET':
        template_data['form'] = UserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
            form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
            if form.is_valid():
                form.save()
                return redirect('accounts.login')
            else:
                template_data['form'] = form
                return render(request, 'accounts/signup.html',
                    {'template_data': template_data})


def password_reset(request):
    template_data = {}
    template_data['title'] = 'Password Reset'

    if request.method == "POST":
        if "email" in request.POST and "new_password" not in request.POST:

            email = request.POST.get("email")
            user = User.objects.filter(email=email).first()

            if user:
                request.session["reset_email"] = email
                template_data["message"] = "We recognize you as a registered user!"
                template_data["email"] = email
            else:
                template_data["error"] = "This email is not registered!"

        elif "new_password" in request.POST and "confirm_password" in request.POST:

            email = request.session.get("reset_email")
            user = User.objects.filter(email=email).first()

            if user:
                new_password = request.POST["new_password"]
                confirm_password = request.POST["confirm_password"]

                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    del request.session["reset_email"]


                    template_data["success"] = True
                    template_data["message"] = "Your password was successfully updated!"
                else:
                    template_data["error"] = "Passwords do not match!"
            else:
                template_data["error"] = "Session expired. Please try again."

    return render(request, "accounts/password_reset.html", {"template_data": template_data})
