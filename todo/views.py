from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserLoginForm, TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, 'You have successfully sign up')
            return redirect('current')
        else:
            messages.error(request, 'Registration Error')
    else:
        form = UserRegisterForm()
    return render(request, 'todo/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'todo/login.html', {'form': form})


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current')
    else:
        form = TodoForm()
    return render(request, 'todo/create_todo.html', {'form': form, })


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=True)
    return render(request, 'todo/current.html', {'todos': todos})


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(
        user=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'todo/completed.html', {'todos': todos})


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('current')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/view_todo.html', {'todo': todo, 'form': form})


@login_required
def complete(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed_date = timezone.now()
        todo.save()
        return redirect('current')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')
