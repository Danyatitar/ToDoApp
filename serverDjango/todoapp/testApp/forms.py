from datetime import date

from django import forms

from .models import Category

WAITING = 'Waiting'
IN_PROGRESS = 'In progress'
COMPLETED = 'Completed'
USER = 'User'  
ADMIN = 'Admin'  
STATUS_CHOICES = [
        (WAITING, 'Waiting'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
]

ROLE_CHOICES= [
    (USER, 'User'),
    (ADMIN, 'Admin'),
]


class RegisterForm(forms.Form):
    name = forms.CharField(
        required=True, 
        min_length=4, 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        required=True, 
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        required=True, 
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )



class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True, 
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        required=True, 
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


class ChangeNameForm(forms.Form):
    name = forms.CharField(
        required=True, 
        min_length=4, 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    
class CategoryForm(forms.Form):
    categoryName = forms.CharField(
        required=True, 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of category'})
    )
    
class CategoryAdminForm(forms.Form):
    categoryName = forms.CharField(
        required=True, 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of category'})
    )
    users = [
            {"id":1,"name": "Sport", "user_id": 1},
            {"id":2,"name": "Work Test", "user_id": 2},
            {"id":3,"name": "University", "user_id": 2},
            {"id":4,"name": "Home", "user_id": 1}
    ]
    
    user_choices = [(user['id'], user['name']) for user in users]
    users = forms.ChoiceField(
        required=True,
        label='User',
        choices=user_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    

class TaskForm(forms.Form):
    title = forms.CharField(
        required=True,
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'})
    )
    description = forms.CharField(
        required=True,
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the description'})
    )
    deadline = forms.DateField(
        required=True,
        label='Deadline',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD','type':'date' }),
        input_formats=['%Y-%m-%d']
    )
    status_choices = STATUS_CHOICES  
    status = forms.ChoiceField(
        required=True,
        label='Status',
        choices=status_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    categories = Category.objects.all()
    category_choices = [(category.id, category.name) for category in categories]
    category = forms.ChoiceField(
        required=True,
        label='Category',
        choices=category_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        print(deadline)
        if deadline <= date.today():
            print(9)
            raise forms.ValidationError("Deadline must be later than today.")
        return deadline
    
    
class UserForm(forms.Form):
    username = forms.CharField(
        required=True, 
        min_length=4, 
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        required=True, 
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    roles_choices =ROLE_CHOICES  
    role = forms.ChoiceField(
        required=True,
        label='Role',
        choices=roles_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )