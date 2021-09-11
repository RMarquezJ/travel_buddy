from django.shortcuts import render, redirect
from .models import Users, Trips
from django.contrib import messages
import bcrypt
from .decorators import login_required
from django.db import IntegrityError

def register(request):

  if request.method == 'GET':
    return render(request,'index.html')

  else:
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']

    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:

      for key,errormsg in errors.items():
        messages.error(request, errormsg)
        
      return redirect('/')
    
    user = Users.objects.create(name=name, email=email, password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())

    request.session['user'] = {
      'id':user.id,
      'name': user.name,
      'email': user.email,
      'avatar':user.avatar
    }

    return redirect('/travels')

def login(request):

    email = request.POST['email']
    password = request.POST['password']

    try:
      user = Users.objects.get(email=email)
      
    except Users.DoesNotExist:
      messages.error(request, 'Usuario y/o contraseña inválidos')
      return redirect('/')

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
      messages.error(request, 'Usuario y/o contraseña inválidos')
      return redirect('/')
    
    request.session['user'] = {
    'id':user.id,
    'name': user.name,
    'email': user.email,
    'avatar':user.avatar
    }
    messages.success(request, f'You have logged in as {user.name}')
    return redirect('/travels')


@login_required
def mainpage(request):

  context = {
    'users' : Users.objects.all(),
    'trips' : Trips.objects.all(),
  }
  
  return render(request, 'travels.html', context)


@login_required
def logout(request):
  del request.session['user']
  return redirect('/')


@login_required
def view(request, tripid):

  context = {
    'trips' : Trips.objects.get(id=tripid),
  }
  
  return render(request, 'view.html', context)

@login_required
def addtrip(request):

  if request.method == 'GET':
    return render(request,'add.html')

  else:

    destination = request.POST['destination']
    plan = request.POST['plan']
    datefrom = request.POST['datefrom']
    dateto = request.POST['dateto']
      
    errors = Trips.objects.basic_validator(request.POST)
    if len(errors) > 0:

      for key,errormsg in errors.items():
        messages.error(request, errormsg)
        
      return redirect('/addtrip')
    
    trip = Trips.objects.create(description=destination, start=datefrom, end=dateto, plan=plan, organizer_id=request.session['user']['id'])

    return redirect('/travels')

@login_required
def delete(request,tripid):
  deletetrip = Trips.objects.get(id=tripid)
  deletetrip.delete()
  return redirect('/travels')

@login_required
def join(request, tripid):
  jointrip = Trips.objects.get(id=tripid)
  usertrip = Users.objects.get(id=request.session['user']['id'])
  jointrip.group.add(usertrip)
  return redirect('/travels')

@login_required
def cancel(request, tripid):
  canceltrip = Trips.objects.get(id=tripid)
  usertrip = Users.objects.get(id=request.session['user']['id'])
  canceltrip.group.remove(usertrip)
  return redirect('/travels')