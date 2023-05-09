from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room,Topic,User,Message
from .forms import RoomForm
from django.contrib.auth import authenticate, login,logout
# Create your views here.


def logIn(request):
  if request.user .is_authenticated:
    return redirect('home')
    
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
      user = User.objects.get(username == username)
    except:
      messages.error(request,"User not found")

    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request,"Username or password doesnot exist")

  context ={}
  return render(request, 'base/login.html',context)


def logOut(request):
  logout(request)
  return redirect('home')

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q)|
    Q(name__icontains=q)|
    Q(description__icontains=q)
    )

  topics = Topic.objects.all()
  room_count = rooms.count()
  context = {'rooms':rooms,'topics':topics,'Totalroom':room_count}
  return render(request,'base/home.html',context)
  # return HttpResponse('Home page')

def rooms(request):
  return HttpResponse('List of rooms')

def room(request, pk):
  room = Room.objects.get(id=pk)
  messages = room.message_set.all()

  if request.method == 'POST':
    message = Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('body')
    )
    return redirect('room', pk=room.id)

  context = {'room':room,'messages':messages}
  return render(request,'base/room.html',context)


@login_required(login_url='login')
def createNewRoom(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')

  context = {'form': form}
  return render(request, 'base/form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)

  if request.user != room.host:
    return HttpResponse('Not authenticated user')

  if request.method =='POST':
    form = RoomForm(request.POST,instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')

  context ={'form': form}
  return render(request, 'base/form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
  room = Room.objects.get(id=pk)

    # if request.user != room.host:
    # return HttpResponse('Not authenticated user')

  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html',{'obj':room})