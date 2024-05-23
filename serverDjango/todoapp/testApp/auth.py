from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import (HttpResponseBadRequest, HttpResponseServerError,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, RegisterForm
from .models import User
from .utils import create_token, hash_password, verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = 10080
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                existing_user = User.objects.get(email=email)
                print(existing_user)
                return JsonResponse({"detail": "Email is already registered"}, status=400)
            except User.DoesNotExist:

                hashed_password = hash_password(password)
                new_user = User.objects.create(name=name, email=email, password=hashed_password, role='user')
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_token(data={"id": new_user.id, "email": new_user.email, "name": new_user.name, "role": new_user.role}, expires_delta=access_token_expires)
                
                
                response = redirect('/tasks')
                response.set_cookie(key="token", value=access_token)
                return response
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        regsierform = RegisterForm()
        data = {'form': regsierform}
        return render(request, 'register.html', data)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                existing_user = User.objects.get(email=email)
                if not verify_password(password, existing_user.password):
                    return JsonResponse({"detail": "Incorrect password"}, status=400)
                
                
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_token(data={"id": existing_user.id, "email": existing_user.email, "name": existing_user.name, "role": existing_user.role}, expires_delta=access_token_expires)
                
                response = redirect('/tasks')
                if(existing_user.role=='Admin'):
                    response = redirect('/administrator/users')
                
                response.set_cookie(key="token", value=access_token)
                return response
                
     
            except User.DoesNotExist:
                return JsonResponse({"detail": "User doesn't exist"}, status=400)
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        loginform = LoginForm()
        data = {'form': loginform}
        return render(request, 'login.html', data)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        loginform = LoginForm()
        data = {'form': loginform}

        response = redirect('/login')
        response.delete_cookie("token")
        return response
    else:
        return HttpResponseBadRequest("Only POST requests are allowed")
# Create your views here.

# def login(request):
    
#     loginform = LoginForm()
#     data = {'form': loginform}
#     return render(request, 'login.html', data)

# def register(request):

#     regsierform = RegisterForm()
#     data = {'form': regsierform}
#     return render(request, 'register.html', data)