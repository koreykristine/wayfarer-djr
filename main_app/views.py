from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from .models import *

# Create your views here.

# Initial View
def splash(request):
    return render(request, 'splash.html')


def edit_profile(request, user_name):
    user = User.objects.get(username=user_name)
    profile = user.profile
    if request.method == 'POST':
        profile_edit_form = Profile_Edit_Form(request.POST, instance=profile)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return redirect ('profile', profile.user.username)
    profile_edit_form = Profile_Edit_Form(instance=profile)
    # cities = City.objects.all()
    context = {'profile_edit_form': profile_edit_form, 'profile': profile}
    return render(request, 'registration/edit.html', context)


def profile(request, user_name):
    user = User.objects.get(username=user_name)
    profile = user.profile
    context = {'profile': profile}
    return render(request, 'registration/profile.html', context)

def myprofile(request):
    user = request.user
    profile = user.profile
    context = {'profile': profile}
    return render(request, 'registration/profile.html', context)


def post(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'posts/detail.html', context)


def home(request):
    return HttpResponse('<h1>Hello there fellow traveler!</h1>')


def about(request):
    user_form = User_Form()
    context = {'form': user_form}
    return render(request, 'about.html', context)


# DAVID'S Semantic Practice
def semantic(request):
    return render(request, 'semantic-ui/semantic.html')
def carousel_test(request):
    return render(request, 'semantic-ui/carousel.html')

def city(request, city_id):
    city = City.objects.get(id=city_id)
    posts = city.post_set.all()
    print('POSTS HERE')
    print(posts)
    context = {"city": city, "posts": posts}
    return render(request, 'cities/detail.html', context)

def create_post(request, city_id):
    if request.method == "POST":
        post_form = Post_Form(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.profile_id = request.user.id
            new_post.city_id = city_id
            new_post.save()
            return redirect('/cities/'+str(city_id))
    post_form = Post_Form()
    context = {"post_form": post_form, "city_id": city_id}
    return render(request, 'posts/create.html', context)



def edit_post(request, post_id):
    pass

def delete_post(request, post_id, city_id):
    doomed_post = Post.objects.get(id=post_id)
    doomed_post.delete()
    return redirect('/cities/'+str(city_id))



def signup(request):
    # if post
    if request.method == "POST":
        # build out data from form
        username_form = request.POST['username']
        email_form = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # validate that passwords match
        if password == password2:
        # check if username exists in db
            if User.objects.filter(username=username_form).exists():
                context = {'error': 'Username is already taken.'}
                return render(request, 'about.html', context)
            else:
                if User.objects.filter(email=email_form).exists():
                    context = {'error':'That email already exists.'}
                    return render(request, 'splash.html', context)
                else: 
                # if everything is ok create account
                    user = User.objects.create_user(
                        username=username_form, 
                        email=email_form, 
                        password=password)
                    user.save()
                    profile_form = Profile_Form()
                    new_profile = profile_form.save(commit = False)
                    new_profile.user_id = user.id
                    new_profile.name = user.username
                    new_profile.save()

                    login(request, user)

                    subject = 'Welcome Wayfarer'
                    message = 'You are registered! Feel free to add your travel experiences and tips to our community of travellers!'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email_form]
                    send_mail(subject, message, email_from, recipient_list)

                    return redirect('/')
        else:
            context = {'error':'Passwords do not match'}
            return render(request, 'splash.html', context)
    else:
        # if not post send message, try again 
        context = {'error':'Your account was not created. Please try again.'}
        return redirect(request, '/')

