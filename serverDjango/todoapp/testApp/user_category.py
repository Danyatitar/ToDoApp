import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import CategoryForm, ChangeNameForm, TaskForm
from .models import Category, Task, User
from .utils import check_user

# Create your views here.

def index(request):
    user = check_user(request)
    changenameform = ChangeNameForm()
    categoryform = CategoryForm()
    if request.method == 'POST':
        parameters = request.POST
 
        new_name = parameters.get('name')
        category_name = parameters.get('categoryName')
        if new_name is not None:
            changenameform = ChangeNameForm(initial={'name': new_name})
            user.name = new_name
            user.save()
        if category_name is not None:
            category = Category(name=category_name,user=user)
            category.save()
    
    else:
        changenameform = ChangeNameForm(initial={'name': user.name})
    
    
    forms= {'changeNameForm': changenameform, 'categoryForm': categoryform}
    categories = Category.objects.filter(user=user.id).all()
    data = {
        "categories": categories,
        "forms":forms
    }
    return render(request, 'user-categories.html', context=data)

@csrf_exempt
def get_category(request, category_id):
    
    user = check_user(request)
    try:
        if request.method == 'PUT':
            if 'application/json' in request.content_type:
                body_unicode = request.body.decode('utf-8')
                data = json.loads(body_unicode)    
                category =  Category.objects.get(id=category_id)
    
                category.name = data['name']
                print(category)
                category.save()
                
                return JsonResponse({"message":"Category was updated"})
            else:
                return None
        elif request.method == 'DELETE':
            category =  Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({"message":"Category was deleted"})
        else:
            category = Category.objects.get(id=category_id)
            category_data = {
                'id': category.id,
                'name': category.name,
            
            }
        
        return JsonResponse(category_data)
        
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    