from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime, time
from django.contrib import messages
from .models import UniUser


def test(request):
    return HttpResponse("Hello, test view.")


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('valueChainApp:home')
            else:
                messages.info(request, 'Username or Password incorrect')
                return render(request, "login.html", )
        context = {}
        return render(request, "login.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('valueChainApp:home')
    else:
        if request.method == 'POST':
            # username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            # user_type = request.POST.get('user_type')
            phone_number = request.POST.get('phone_number')

            user = UniUser.objects.create_user(username=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number)
            user.set_password(password)
            user.save()

            # messages.success(request, 'Account successfully create for ' + user)
            return redirect('userApp:login')
        return render(request, "signup.html")

def logoutUser(request):
    user = request.user
    logout(request)

    return redirect('userApp:login')




def changePass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUserForm(user=request.user, data=request.POST)

            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user = authenticate(request,  password=new_password)
            user.save()

            messages.info(request, 'password successfully changed')
            return redirect('/home/')
    else:
        return redirect('userapp:login')
    form = CreateUserForm()
    context = {'form': form}
    return render(request, "change_password.html", context)