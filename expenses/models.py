from django.db import models
from django.db.models.fields import CharField, FloatField, TextField
from user.models import User
# Create your models here.

CATEGORY_CHOICES = [
    ('equal', 'Equal'),
    ('percentage', 'Percentage'),
    ('exact', 'Exact'),
]

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE, default="unknown")
    expense_amount = models.FloatField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    payer = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    expense = models.ForeignKey(Expense, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='participations', on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    percentage = models.FloatField(default=0.0)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)