from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    data= {'test': 'This is data binding'}
    return render(request, 'index.html',context=data)