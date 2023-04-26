from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("You Tweet has been posted!"))
                return redirect('home')

        
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets": tweets, "form":form})
    else:
         tweets = Tweet.objects.all().order_by("-created_at")
         return render(request, 'home.html', {"tweets": tweets})


def profile_list(request):
    if request.user.is_authenticated:
       profiles = Profile.objects.exclude(user=request.user)
       return render(request, 'profile_list.html', {"profiles": profiles})
    else: 
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
       profile = Profile.objects.get(user_id=pk) 
       tweets = Tweet.objects.filter(user_id=pk)
       

       #post form logic
       if request.method == "POST":
                      #get current user
           current_user_profile = request.user.profile
           #Get from data
           action = request.POST['follow']
           #decide to follow or unfollow      
           if action == "unfollow":
               current_user_profile.follows.remove(profile)
           elif action == "follow":
               current_user_profile.follows.add(profile)
           #save the profile
           current_user_profile.save()     
       return render(request, "profile.html", {"profile": profile, "tweets":tweets})
       
    else: 
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           messages.success(request, ("You have logged In!"))
           return redirect('home')
       else:
           messages.success(request, ("There was an error in logging In!"))
           return redirect('login')
       
    else:    
        return render(request, "login.html", {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out.")) 
    return redirect('home')