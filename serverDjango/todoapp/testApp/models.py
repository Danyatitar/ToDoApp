import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


class User(models.Model):
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email])
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES)

    def clean(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValidationError("Invalid email address format")

        if len(self.name) < 4:
            raise ValidationError("Name must be at least 4 characters long")

        if self.role not in dict(self.ROLES).keys():
            raise ValidationError("Invalid role. Must be 'admin' or 'user'")

class Task(models.Model):
    STATUS_CHOICES = (
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('waiting', 'Waiting'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='tasks', on_delete=models.DO_NOTHING)

    def clean(self):
        if len(self.title) < 4:
            raise ValidationError('Title must be at least 4 characters long')

        if self.deadline < date.today():
            raise ValidationError("Deadline must be later than or equal to today's date")

        if self.status not in dict(self.STATUS_CHOICES).keys():
            raise ValidationError('Invalid status. Must be one of: "in progress", "completed", "waiting"')

class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
