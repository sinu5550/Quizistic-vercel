from django.db import models
from category.models import Category
from django.contrib.auth.models import User
# from .constants import RATINGS
# Create your models here.
RATINGS = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    choice = models.CharField(choices=RATINGS,max_length=20)
    body = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.quiz.title}"
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    opt_1= models.CharField(max_length =250)
    opt_2= models.CharField(max_length =250)
    opt_3= models.CharField(max_length =250)
    opt_4= models.CharField(max_length =250)
    time_limit = models.IntegerField()
    right_opt = models.CharField(max_length=100)

    def __str__(self):
        return self.question
    

class UserAnswerSubmit(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    right_ans = models.CharField(max_length = 250)
    
class userQuizAttempts(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attemp_time = models.DateTimeField(auto_now_add=True)
    