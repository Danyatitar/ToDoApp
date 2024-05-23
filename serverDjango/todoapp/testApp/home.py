
import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import ChangeNameForm, TaskForm
from .models import Category, Task, User
from .utils import check_user

# Create your views here.

def index(request):
    
    user = check_user(request)
    changenameform = ChangeNameForm()
    taskform = TaskForm()
    if request.method == 'POST':

            parameters = request.POST
            new_name = parameters.get('name')
            title = parameters.get('title')
            if new_name is not None:
                changenameform = ChangeNameForm(initial={'name': new_name})
                user.name = new_name
                user.save()
            if title is not None:
                category = Category.objects.get(id=parameters.get("category"))
                task = Task(title=title, description = parameters.get("description"), deadline =datetime.strptime(parameters.get("deadline"), '%Y-%m-%d').date(), status=parameters.get("status"), user=user,category=category)
                task.save()
        
            

    
    else:
        changenameform = ChangeNameForm(initial={'name': user.name})
        
    forms= {'changeNameForm': changenameform, 'taskForm': taskform}
    tasks = Task.objects.filter(user=user.id).select_related('category').all()

        
    data = {
        "tasks": tasks,
        "forms":forms
    }
    return render(request, 'home-user.html', context=data)


@csrf_exempt
def get_task(request, task_id):
    user = check_user(request)
    try:
        if request.method == 'PUT':
            if 'application/json' in request.content_type:
                body_unicode = request.body.decode('utf-8')
                data = json.loads(body_unicode)    
                task =  Task.objects.get(id=task_id)
    
                task.title = data['title']
                task.description = data['description']
                task.deadline = data['deadline']
                task.status = data['status']
                task.category_id= data['category_id']
                task.save()
                
                return JsonResponse({"message":"Task was updated"})
            else:
                return None
        elif request.method == 'DELETE':
            task =  Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({"message":"Task was deleted"})
        else:
            task = Task.objects.filter(id=task_id).select_related('category').values('id', 'title', 'description', 'deadline', 'status', 'user_id', 'category_id', 'category__name').first()
        
            category_info = {
                    'id': task['category_id'],
                    'name': task['category__name']
                }
            task['category'] = category_info
            del task['category_id']
            return JsonResponse(task, safe=False)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    
# def update_task(request, task_id):
#     user = check_user(request)
#     try:
#         task = Task.objects.filter(id=task_id).first()
#         if request.method == 'PUT':
#             print(request.PUT)
        
#         return JsonResponse(task, safe=False)
#     except Task.DoesNotExist:
#         return JsonResponse({'error': 'Task not found'}, status=404)