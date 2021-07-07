from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2'] :
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Username already taken .Please choose a new username.'})
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not match.'})
def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username & password didnot match!'})
        else:
            login(request,user)
            return redirect('current_todos')
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
@login_required
def create_todos(request):
    if request.method == "GET":
        return render(request,'todo/create_todos.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('current_todos')
        except:
            return render(request,'todo/create_todos.html',{'form':TodoForm(),'error':'Bad data!!!Try again.'})
@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/current_todos.html',{'todos':todos})
@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/completed_todos.html',{'todos':todos})
@login_required
def view_todos(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request,'todo/view_todos.html',{'todo':todo,'form':form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request,'todo/view_todos.html',{'todo':todo,'form':form,'error':'Bad information.'})
@login_required
def complete_todos(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current_todos')
@login_required
def delete_todos(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('current_todos')



