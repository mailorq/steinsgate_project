import logging
import os

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from . import services
from .forms import LoginForm, RegisterForm

logger = logging.getLogger(__name__)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = services.register_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            request.session['pending_user_id'] = user.id
            return redirect('email_verification')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {"form": form})


def email_verification_view(request):
    pending_user_id = request.session.get('pending_user_id')
    if not pending_user_id:
        return redirect('register')

    user = User.objects.filter(id=pending_user_id, is_active=False).first()
    if user is None:
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code', '')

        if not code.isdigit():
            return render(request, 'users/email_verification.html', {
                'error': 'Код должен содержать только цифры.'
            })

        try:
            services.verify_email(user=user, code=code)
        except services.VerificationError as error:
            return render(request, 'users/email_verification.html', {'error': str(error)})

        request.session.pop('pending_user_id', None)
        login(request, user)
        return redirect('steins_gate_page')

    return render(request, 'users/email_verification.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = services.authenticate_user(
                request=request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                logger.debug(f"User logged in , user={user.username}")
                return redirect("steins_gate_page")
            form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {"form": form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect("steins_gate_page")
    return render(request, 'users/logout.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {
        "user": request.user,
        "profile": request.user.profile,
    })


@login_required
def change_nickname(request):
    if request.method == 'POST':
        new_nickname = request.POST.get('nickname')
        if new_nickname and len(new_nickname) <= 50:
            services.update_nickname(user=request.user, nickname=new_nickname)
            return redirect('profile')
    return render(request, 'users/change_nickname.html')


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_AVATAR_SIZE = 8 * 1024 * 1024

@login_required
def change_avatar(request):
    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar = request.FILES['avatar']

        if avatar.size > MAX_AVATAR_SIZE:
            return render(request, 'users/change_avatar.html',
                          {'error': 'File too large. Max 8 MB'})

        ext = os.path.splitext(avatar.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return render(request, 'users/change_avatar.html',
                          {'error': 'Only JPG, PNG, GIF, WEBP allowed'})

        services.update_avatar(user=request.user, avatar=avatar)
        return redirect('profile')

    return render(request, 'users/change_avatar.html')


@login_required
def profile_settings(request):
    return render(request, "users/settings.html")
