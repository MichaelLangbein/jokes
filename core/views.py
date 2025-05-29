from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def homePage(req):
    return render(req, 'homePage.html')


def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'loginPage.html')
    else:
        return render(request, 'loginPage.html')


def logoutUser(request):
    logout(request)
    return redirect('home')
