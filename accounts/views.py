from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from reci.models import recipes
from django.contrib.auth import authenticate
from .models import Profile
from django.core.mail import send_mail


def index(request):
    return render(request,'index.html')

# from django.views.decorators.csrf import csrf_exempt
def index(request):
    recipes=recipes.objects.all()
    return render(request,'index.html',{'recipes':recipes})

def signup(request):
    if  request.method=="POST":
        secondname=request.POST['secondname']
        email=request.POST['email']
        firstname=request.POST['firstname']
        password=request.POST['password']
        if(User.objects.filter(username=email)).exists():
            messages.error(request,"Email already exists!")
            return render(request,'sign-up.html')
           
        else:
            user=User.objects.create_user(first_name=firstname,last_name=secondname,email=email,username=email,password=password)
            user.save()
            send_mail(
            'Welcome to oishii',
            'Welcome to Oishi we are excited that you joned!    ',
            'oishirecipes12@gmail.com',
            [email],
            fail_silently=False,
                                )
            
            return render(request,'sign-in.html')
        

    else:

        return render(request,'sign-up.html') 

    # csrf_exempt
def signin(request):
     if  request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            prof=Profile.objects.filter(user=request.user)
            if not prof :
                usr=Profile()
                usr.user=request.user
                usr.save()
                
            return redirect("/")
        else:
             messages.error(request,"Invalid username or password")
             return render(request,'sign-in.html')



     else:    
        return render(request,'sign-in.html')
def logout(request):
    auth.logout(request)
    return redirect('/')