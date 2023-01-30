from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
# Create your views here.


def home(requests):
    if requests.user.is_anonymous:
        return redirect("/login")
    return render(requests, 'home.html')


def loginUser(requests):
    if requests.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # A backend authenticated the credentials
            login(requests, user)
            return redirect('/base')
        else:
            # No backend authenticated the credentials
            return render(requests, 'login.html')

    return render(requests, 'login.html')


def logoutUser(requests):
    logout(requests)
    return redirect('/login')


def base(requests):
    # if requests.method == 'POST':
    #     print('done post request')
    if requests.method == 'POST':
        name = requests.POST.get('name')
        email = requests.POST.get('email')
        Mobile_Number = requests.POST.get('Mobile Number')
        Income = requests.POST.get('Income')
        Nofr = requests.POST.get('Nofr')
        Nobr = requests.POST.get('Nobr')
        ppor = requests.POST.get('PPOR')
        place = requests.POST.get('place')
        print(name, email, Mobile_Number, Income, Nofr, Nobr, ppor, cars)
    return render(requests, 'index.html')
