from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")

@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if UserDetails.objects.filter(username = username).exists():
            return HttpResponse("Username already exists!")
        user = UserDetails(username = username, email = email, password = password)
        user.save()
        return redirect("login")
    return render(request, "signup.html")

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = UserDetails.objects.get(username = username, password = password)
            return render(request, "success.html", {"user": user})
        except Exception as e:
            return HttpResponse("Invalid credentials!")
    return render(request, "login.html")