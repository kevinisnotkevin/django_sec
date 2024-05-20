from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import User, Profile
from .forms import SignUpForm, LoginForm, EditProfileForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверная почта или пароль')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'account/profile.html', {'profile': profile, 'user': user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user.username,
                               request.POST, request.FILES)
        if form.is_valid():
            about = form.cleaned_data["about"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about = about
            if image:
                profile.image = image
            profile.save()
            return redirect("profile", username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, "account/edit_profile.html", {'form': form})