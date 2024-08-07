from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError

from django.utils import timezone

from .forms import TaskForm
from .models import Task

#from django.http import HttpResponse -> Util para comenzar


# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
            })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    )

                user.save()
                login(request, user)

                # return HttpResponse("Exito al registrar") -> Util para comenzar
                return redirect('tasks')

            #- Es una buena practica usar una excepcion especifica para manejar errores
            #- en lugar de usaruna excepcion generica como en el codigo anterior.
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': "El usuario ya existe"
                    })
                #return HttpResponse("EL usuario ya existe") -> Util para comenzar

        return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': "Las contraseñas no coinciden"
                    })
        #return HttpResponse("pass do not match") -> Util para comenzar


#- @login_required sirve para verificar que el usario este logeado y evitar errores en el backend.

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
        })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
        })
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm()
            })

    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': "Por favor, rellene todos los campos"
                })


@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task.detail.html', {
            'task': task,
            'form': form})

    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task.detail.html', {
                'task': task,
                'form': form,
                'error': "Por favor, rellene todos los campos"
                })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin (request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
            })

    else:
        user = authenticate(request,
                     username=request.POST['username'],
                     password=request.POST['password']
                     )

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': "Usuario o contraseña incorrectos"
                })
        else:
            login(request, user)
            return redirect('tasks')

