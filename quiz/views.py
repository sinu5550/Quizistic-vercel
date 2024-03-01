from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from . import models
from . import forms
from category.models import Category
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# Create your views here.

@login_required
def all_quiz_view(request,category_slug=None):

    quizzes = models.Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()
    
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        quizzes = models.Quiz.objects.filter(category = category)
    categories = Category.objects.all()
    context ={"quizzes":quizzes, "categories":categories}


    return render(request,'all_quiz.html',context)

@login_required
def question_view(request,q_id):
    request.session['question_counter'] = 1
    quiz = models.Quiz.objects.get(id=q_id)
    # models.UserAnswerSubmit.objects.filter(user=request.user, question__quiz=quiz).delete()
    question = models.Question.objects.filter(quiz=quiz).order_by('id').first()
    
    lastAttemp = None
    futureTime = None
    hoursLimit = 24
    countAttemp = models.userQuizAttempts.objects.filter(user=request.user, quiz = quiz).count()
    if countAttemp == 0:
        models.userQuizAttempts.objects.create(user = request.user, quiz=quiz)
    else:
        lastAttemp= models.userQuizAttempts.objects.filter(user = request.user, quiz=quiz).order_by('-id').first()
        futureTime = lastAttemp.attemp_time+ timedelta (hours = hoursLimit)
        if lastAttemp and timezone.now() < futureTime :
            remaining_time = futureTime - timezone.now()
            minutes, seconds = divmod(remaining_time.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            remaining_time_str = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
            msg = f'You already attempted this quiz. Please come back after <b>{remaining_time_str}.</b>'
            messages.warning(request,mark_safe(msg) )
            return all_quiz_view(request,None)
        models.UserAnswerSubmit.objects.filter(user=request.user, question__quiz=quiz).delete()
        lastAttemp.delete()
        models.userQuizAttempts.objects.create(user=request.user, quiz=quiz)
    
    return render(request,'questions.html',{'ques':question,'quiz': quiz, 'lastAttemp':futureTime,})


def send_result_email(user,score,title,total_ques, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'score' : score,
            'title' : title,
            'total_ques' : total_ques,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@login_required
def submit_answer_view(request,q_id,ques_id):
    if request.method =='POST':
        quiz = models.Quiz.objects.get(id=q_id)
        question = models.Question.objects.filter(quiz=quiz,id__gt=ques_id).exclude(id= ques_id).order_by('id').first()      
        
        if 'skip' in request.POST:
           
            ques = models.Question.objects.get(id=ques_id)
            user = request.user
            answer = 'Not Submitted'
            models.UserAnswerSubmit.objects.create(
                user=user,question=ques,right_ans=answer
            )
            question_counter = int(request.session.get('question_counter', 1))
            question_counter += 1
            request.session['question_counter'] = question_counter

            if question:
                return render(request,'questions.html',{'ques':question,'quiz': quiz})
            else:
                return redirect(reverse('quiz-result', args=[quiz.id, user.id, q_id]))
        
        else:
            ques = models.Question.objects.get(id=ques_id)
            user = request.user
            answer = request.POST.get('answer', None)
            if answer is not None:
                models.UserAnswerSubmit.objects.create(
                user=user, question=ques, right_ans=answer
                )
            else:
                messages.warning(request, 'Please select an option before submitting.')
                return render(request, 'questions.html', {'ques': ques, 'quiz': quiz})
            
            question_counter = int(request.session.get('question_counter', 1))
            question_counter += 1
            request.session['question_counter'] = question_counter

            if question:
                return render(request,'questions.html',{'ques':question,'quiz': quiz})
            else:
                return redirect(reverse('quiz-result', args=[quiz.id, user.id, q_id]))
        
        
        
        
    else:
        return redirect('all_quiz')

def result_after_quiz(request, quiz_id, user_id, q_id):
    
    user_model = get_user_model()
    quiz = get_object_or_404(models.Quiz, id=quiz_id)
    user = get_object_or_404(user_model, id=user_id)
    result = models.UserAnswerSubmit.objects.filter(user=request.user,question__quiz=quiz)
    skipped = models.UserAnswerSubmit.objects.filter(user=request.user,right_ans='Not Submitted',question__quiz=quiz).count()
    attemped = models.UserAnswerSubmit.objects.filter(user=request.user,question__quiz=quiz).exclude(right_ans='Not Submitted').count()
    rightAns= 0
    for r in result:
        if r.question.right_opt == r.right_ans:
            rightAns+=1
    send_result_email(user, rightAns,quiz.title,result.count,"Quiz Result", "result_email.html")

    messages.success(request,'Your Quiz result has been sent to you Mail !')
    return render(request,'quiz_result.html',{'result':result,'skipped':skipped,'attemped':attemped,'rightAns':rightAns,'quiz_id': q_id,'quiz':quiz})

@login_required   
def result(request):
    result = models.UserAnswerSubmit.objects.filter(user=request.user)
    skipped = models.UserAnswerSubmit.objects.filter(user=request.user,right_ans='Not Submitted').count()
    attemped = models.UserAnswerSubmit.objects.filter(user=request.user).exclude(right_ans='Not Submitted').count()
    rightAns= 0
    for r in result:
        if r.question.right_opt == r.right_ans:
            rightAns+=1
    return render(request,'quiz_result.html',{'result':result,'skipped':skipped,'attemped':attemped,'rightAns':rightAns})




class RatingsView(DetailView):
    model = models.Quiz
    pk_url_kwarg = 'id'
    template_name = 'ratings.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        quiz = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.quiz = quiz
            new_comment.user = request.user
            new_comment.save()
        return redirect('ratings', id=quiz.id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object 
        comments = quiz.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context



