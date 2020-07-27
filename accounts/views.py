from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method == 'POST':
        #User wants to sign up with info
        if request.POST['password1'] == request.POST['password2']:
            # if User.objects.get(email=request.POST['email']): TODO: figure out email check and auth
            #     return render(request, 'accounts/signup.html', {'error':"E-mail is already in use. Did you forget your password?"})
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error':"Username has already been taken"})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':"Passwords do not match. Passwords must match"})
    else:
            #user wants to enter info
        return render(request, 'accounts/signup.html')



def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Username or Password is incorrect'})

    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
