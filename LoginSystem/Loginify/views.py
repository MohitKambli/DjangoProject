from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserDetails
from .serializers import UserDetailsSerializer
import json

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

@csrf_exempt
def get_all_users(request):
    if request.method == "GET":
        users = UserDetails.objects.all()
        serializer_data = UserDetailsSerializer(users, many = True)
        return JsonResponse(serializer_data.data,safe=False)

@csrf_exempt
def get_user_by_email(request, email):
    if request.method == "GET":
        try:
            user = UserDetails.objects.get(email = email)
            serializer_data = UserDetailsSerializer(user)
            return JsonResponse(
                {
                    "success":True,
                    "Data":serializer_data.data
                }, 
                status = 200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success":False,
                    "error":str(e)
                }, 
                status = 400
            )

@csrf_exempt
def update_user(request, email):
    if request.method in ["PUT", "PATCH"]:
        try:
            user = UserDetails.objects.get(email = email)
            input_data = json.loads(request.body)
            serializer_data = UserDetailsSerializer(user, data=input_data, partial=(request.method == "PATCH"))
            if serializer_data.is_valid():
                serializer_data.save()
                return JsonResponse(
                    {
                        "Success":True,
                        "message":"Data Updated Successfully",
                        "Updated Data ": serializer_data.data
                    }, 
                    status = 200
                )
        except Exception as e:
            return JsonResponse(
                {
                    "success":False,
                    "Error":str(e)
                }, 
                status = 400
            )

@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(email = email)
            user.delete()
            return JsonResponse(
                {
                    "Success":True,
                    "message":"Data Deleted Successfully",
                }, 
                status = 200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "success":False,
                    "Error":str(e)
                }, 
                status = 400
            )