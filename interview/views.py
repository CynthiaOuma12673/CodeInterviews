from turtle import title
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.http  import HttpResponseRedirect,Http404
from . forms import UpdateUserForm, UpdateUserProfileForm, UserRegisterForm,QuestionForm
from .models import Question,Profile
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'all-quiz/home.html')

def register(request):
    if request.user.is_authenticated:
    #redirect user to the profile page
        return redirect('home')
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
    return render(request,"registration/register.html",{'form':form})

@login_required(login_url='login')
def quiz(request):
    current_user=request.user
    quiz = Question.objects.all()
    return render(request,"all-quiz/quiz.html",{'quiz':quiz,'current_user':current_user})

@login_required(login_url='login')
def profile(request, username):
    current_user=request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)

    return render(request, 'all-quiz/profile.html', {'user_form':user_form,'profile_form':profile_form})

@login_required(login_url='login')
def new_quiz(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.admin = request.user
            quiz.save()
            return HttpResponseRedirect(reverse("quiz"))
    else:
        form = QuestionForm()
    return render(request, 'all-quiz/new-quiz.html', {'form': form})

@login_required(login_url='login')
def user(request,id):
    current_user = request.user
    quiz = Question.objects.get(id=id)
    request.user.profile.question = quiz
    request.user.profile.save()
    
    return render(request, 'all-quiz/user.html', {'quiz': quiz,'current_user':current_user})
    
    
@login_required(login_url='login')   
def search_quiz(request):
    current_user= request.user
    if request.method == 'GET':
        name = request.GET.get("name")
        quizs = Question.objects.filter(name__icontains=name).all()

    return render(request, 'all-quiz/search.html', {'quizs': quizs,'current_user':current_user})

@login_required(login_url='login')
def update_quiz(request,id):
    title = 'UPDATE QUESTION'
    instance= Question.objects.get(id=id)
    if request.method=='POST':
        form = QuestionForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
        messages.success(request, ('Question Updated Successfullly'))
        return redirect('quiz')
    else:
        form = QuestionForm(instance=instance)
    return render(request,'all-quiz/new-quiz.html',{'form':form,'title':title})

def user_profile(request, username):
    current_user=request.user       
    user_poster = get_object_or_404(User, username=username)
    
    if request.user == user_poster:
        return redirect('profile', username=request.user.username)
    return render(request, 'all-quiz/member.html', {'user_poster': user_poster,'current_user':current_user})