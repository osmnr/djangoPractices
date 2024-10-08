from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import UsersTodoList
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def todoList(request):
    session_key = request.session.session_key
    if(not session_key):
        request.session.create()
        session_key = request.session.session_key

    if request.method == 'POST':
        newTask = request.POST.get('taskSubject')
        if len(newTask)<=3:
            messages.error(request, 'The task should have at least 4 characters.')
        else:
            if request.user.is_authenticated:
                myUser = request.user
                a = UsersTodoList(taskName=newTask, sessionKey=session_key, user=myUser)
                a.save()
            if not request.user.is_authenticated:
                a = UsersTodoList(taskName=newTask, sessionKey=session_key)
                a.save()

    if request.user.is_authenticated:
        myUser = request.user
        pageFilter = request.GET.get('filter')
        if pageFilter:
            if pageFilter.lower() == 'undone':
                taskList = UsersTodoList.objects.filter(user=myUser, isDeleted=False, isDone=False).order_by('updatedDate','id')
            elif pageFilter.lower() == 'done':
                taskList = UsersTodoList.objects.filter(user=myUser, isDeleted=False, isDone=True).order_by('updatedDate','id')
            elif pageFilter.lower() == 'deleted':
                taskList = UsersTodoList.objects.filter(user=myUser, isDeleted=True).order_by('updatedDate','id')
            elif pageFilter.lower() == 'other' and myUser.is_staff:
                taskList = UsersTodoList.objects.all().exclude(user=myUser).order_by('updatedDate','id')
            else:
                return redirect('todoList:index')
        else:
            taskList = UsersTodoList.objects.filter(user=myUser,isDeleted=False).order_by('isDone','updatedDate','id')
    
    
    else:
        pageFilter = request.GET.get('filter')
        if pageFilter:
            if pageFilter.lower() == 'undone':
                taskList = UsersTodoList.objects.filter(sessionKey=session_key, isDeleted=False, isDone=False).order_by('updatedDate','id')
            elif pageFilter.lower() == 'done':
                taskList = UsersTodoList.objects.filter(sessionKey=session_key, isDeleted=False, isDone=True).order_by('updatedDate','id')
            elif pageFilter.lower() == 'deleted':
                taskList = UsersTodoList.objects.filter(sessionKey=session_key, isDeleted=True).order_by('updatedDate','id')
            else:
                return redirect('todoList:index')
        else:
            taskList = UsersTodoList.objects.filter(sessionKey=session_key,isDeleted=False).order_by('isDone','updatedDate','id')


    daysKeep = 3
    past_date_before_daysKeep = timezone.now() - timedelta(days = daysKeep)
    ## Todolist.objects.filter(updatedDate__lte=daysKeep) ## bunu kullanamadık.

    filteredList = [i for i in taskList if (i.isDone and i.updatedDate >= past_date_before_daysKeep) or not i.isDone ]

    # yukarıdaki tek satıra alternatif olarak:
    """ filteredList = []
    for i in taskList:
        if (i.isDone  and i.updatedDate >= past_date_before_daysKeep) or not i.isDone:
            filteredList.append(i)
         """
    
    data = {
        'filteredList':filteredList,
        'sessionId':session_key,
    }
    return render(request, 'todoList/todoList.html',data)


def updateTodoItem(request, pk):
    try:
        todoItem = UsersTodoList.objects.get(pk=pk)
        if todoItem.isDone:
            todoItem.isDone = False
        else:
            todoItem.isDone = True
        todoItem.save()
        return redirect('todoList:index')
    except UsersTodoList.DoesNotExist:
        return redirect('todoList:index')
    

def deletedTodoItem(request, xxx):
    try:
        todoItem = UsersTodoList.objects.get(pk=xxx)
        if todoItem.isDeleted == True and request.user.is_staff:
            todoItem.isDeleted = False
        else:
            todoItem.isDeleted = True
        todoItem.save()
        return redirect('todoList:index')
    except UsersTodoList.DoesNotExist:
        return redirect('todoList:index')
    

