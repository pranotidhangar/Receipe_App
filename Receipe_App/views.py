from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def receipe(request):
    if request.method == 'POST':
        data = request.POST
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
        Receipe.objects.create(
            receipe_img  = receipe_img ,
            receipe_name = receipe_name,
            receipe_desc = receipe_desc,
        ) 

    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains=request.GET.get('search'))
    context = {'receipe':queryset}
    return render(request,'receipe.html', context)
def del_receipe(request,id):
    Receipe.objects.get(id=id).delete()
    return redirect('receipe')
def update_receipe(request,id):    
    queryset = Receipe.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
        
        queryset.receipe_name = receipe_name
        queryset.receipe_desc = receipe_desc
        if receipe_img:
            queryset.receipe_img = receipe_img

        queryset.save()
        return redirect('receipe')    
    context = {'receipe':queryset}
    return render(request, 'update_receipe.html', context)


def LoginPage(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'Invalid Username🙁' )
            return redirect('/login')

        user = authenticate(username=username, password=password)


        if user is None:
            messages.info(request,'Invalid Password🙁' )
            return redirect('/login')

        else:
          login(request, user)
          return redirect('receipe')

     return render(request, 'Login.html')
          
def LogoutPage(request):
    logout(request)
    return redirect('/login')          
def Register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'Username already Taken🙃' )
            return redirect('Register')
        
        user = User.objects.create(
            first_name= first_name,
            last_name = last_name,
            username=username,
        )
        user.set_password(password)  
        user.save()
        messages.info(request, 'Account Created Successfully😃')
        return redirect('Register')
    return render(request, 'Register.html')    