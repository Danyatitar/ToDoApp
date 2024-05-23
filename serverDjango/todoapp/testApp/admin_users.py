import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import ChangeNameForm, TaskForm, UserForm
from .models import Category, Task, User
from .utils import check_user, hash_password


def index(request):
    user = check_user(request)
    changenameform = ChangeNameForm()
    userform = UserForm()
    if request.method == 'POST':

            parameters = request.POST
            new_name = parameters.get('name')
            username = parameters.get('username')
            if new_name is not None:
                changenameform = ChangeNameForm(initial={'name': new_name})
                user.name = new_name
                user.save()
            if username is not None:
                
                new_user = User(name=username, password = hash_password('12345'),email=parameters.get('email'), role=parameters.get('role'))
                new_user.save()
        
            

    
    else:
        changenameform = ChangeNameForm(initial={'name': user.name})
    users =  User.objects.all()
    forms= {'changeNameForm': changenameform, 'userForm': userform}
    data={"users":users, "forms":forms}
    
    return render(request, 'admin_users.html',data)

@csrf_exempt
def get_user(request, user_id):
       
    user = check_user(request)
    try:
        if request.method == 'PUT':
            if 'application/json' in request.content_type:
                body_unicode = request.body.decode('utf-8')
                data = json.loads(body_unicode)    
                updated_user =  User.objects.get(id=user_id)
    
                updated_user.name = data['name']
                updated_user.email = data['email']
                updated_user.role = data["role"]
                updated_user.save()
                
                return JsonResponse({"message":"User was updated"})
            else:
                return None
        elif request.method == 'DELETE':
            deleted_user =  User.objects.get(id=user_id)
            deleted_user.delete()
            return JsonResponse({"message":"user was deleted"})
        else:
            existing_user = User.objects.get(id=user_id)
            user_data = {
                'id': existing_user.id,
                'name': existing_user.name,
                'email': existing_user.email,
                'role': existing_user.role
            
            }
        
        return JsonResponse(user_data)
        
    except Category.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


