from django.shortcuts import render
from quiz.models import Quiz
from category.models import Category
from account.models import UserProfile

def home (request,category_slug=None):
    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        quizzes = Quiz.objects.filter(category = category)
    categories = Category.objects.all()
    context ={"quizzes":quizzes, "categories":categories}
    return render(request,'home.html',context)

