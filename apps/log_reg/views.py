from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):

    return render(request, 'log_reg/index.html')

def register(request):
    #invoke the method from models and capture
    if request.method == 'POST':

        response_from_model = User.objects.register_user(request.POST)
    print ('*')*50
    print response_from_model
    if response_from_model['status']:
        request.session['user_id'] = response_from_model['user'].id
        request.session['name'] = response_from_model['user'].name
        return redirect('main:index')
    else:
        print ('8')*50
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('users:index')

def login(request):
    if request.method == 'POST':
        response_from_model = User.objects.login_user(request.POST)

    if response_from_model['status']:
        request.session['user_id'] = response_from_model['user'].id
        request.session['name'] = response_from_model['user'].name
        print request.session['name']
        return redirect('main:index')
    else:
        messages.error(request, response_from_model['error'])
        return redirect('users:index')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')

    else:
        context={
        'id' : id
        }
    return redirect('main:index')

def logout(request):
    request.session.clear()
    return redirect('users:index')
    pass
