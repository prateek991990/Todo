from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # To Create a new Form
from django.contrib.auth.models import User  # to Create a New User
from django.db import IntegrityError  # When Username is not available
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form': AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form': authenticate(), 'error': 'Username and Password '
                                                                                             'did not match '})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user  # Only valid user can add to #
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad Data'})


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html',
                              {'form': UserCreationForm(), 'error': 'Username has already been taken'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Your Passwords did not '
                                                                                             'match'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def compleatedtodos(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/compleatedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad Info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

