from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def users(request):
    context = {
        'user_list': User.objects.all()
    }
    return render(request, 'users.html', context)

def register(request):
    errors = User.objects.validator(request.POST)

    if(len(errors)):
        for tag, error in errors.items():
            messages.error(request,error, extra_tags=tag)
        return redirect('home')
    else:
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        hashed_password = bcrypt.hashpw(request.POST.get('password').encode(),bcrypt.gensalt()).decode()
        User.objects.create(first_name=firstName, last_name=lastName, email=email, password=hashed_password)
        user = User.objects.last()
        return redirect ('success', id=user.id)
    
def success(request, id):
    context ={
        'user': User.objects.get(id=id)
    }
    return render(request, 'success.html', context)

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('users')

def login(request):
    if request.method == "POST":
        errors = User.objects.loginValidator(request.POST)
        if (len(errors)):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        
        user = User.objects.get(email=request.POST['loginEmail'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("User Password Matches")
            request.session['id']=user.id
            request.session['first_name']=user.first_name
            return redirect('/book/add_book')
        else:
            print("User Password Match Fails")
            return redirect("/")