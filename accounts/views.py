from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from accounts.forms import ProfileImageUploadForm
from accounts.models import GENDER_CHOISES
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from .utils import save_uploaded_file, check_uploaded_image
import re


def index_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST['login'].lower()
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')

            messages.warning(request, 'Неверный логин или пароль')
            return redirect('login')
        else:
            return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    account = Account.objects.get(user=request.user)
    context = {
        'account': account,
        'gender': GENDER_CHOISES.get(account.gender)
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def signup_view(request):
    def validate_username(string):
        pattern = re.compile(r'^[A-Za-z0-9_]+$')
        return bool(pattern.match(string))

    def validate_name(string):
        pattern = re.compile(r'^[A-Za-zА-Яа-яёЁ]+$')
        return bool(pattern.match(string))

    context = {}

    if request.method == 'POST':

        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        username = request.POST.get('login').lower()
        email = request.POST.get('email').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'username': username,
            'email': email
        }

        # check firstname and lastname
        if not validate_name(first_name) or not validate_name(last_name):
            messages.warning(request, 'Имя и фамилия должны состоять только из русских или латинских букв')
            return render(request, 'accounts/signup.html', context=context)

        # check username
        if not validate_username(username):
            messages.warning(request, 'Логин должен состоять только из латинских букв, цифр или символа подчеркивания')
            return render(request, 'accounts/signup.html', context=context)

        # check unique username
        if User.objects.filter(username=username).exists():
            messages.warning(request, f'Логин {username} уже занят')
            return render(request, 'accounts/signup.html', context=context)

        # check unique email
        if User.objects.filter(email=email).exists():
            messages.warning(request, f'Такой email уже зарегистрирован')
            return render(request, 'accounts/signup.html', context=context)

        # check age
        if age:
            try:
                age = int(age)
            except ValueError:
                messages.warning(request, 'Возраст должен состоять из цифр')
                return render(request, 'accounts/signup.html', context=context)

        # check equals passwords
        if password1 and password2 and password1 != password2:
            messages.warning(request, 'Пароли не совпадают')
            return render(request, 'accounts/signup.html', context=context)

        # validate password
        try:
            valid = validate_password(password1)
        except ValidationError as error:
            for e in error:
                messages.warning(request, e)

        # gender to int
        if gender == 'male':
            gender = 1
        else:
            gender = 0

        # create User model
        user = User.objects.create_user(username=username, email=email, password=password2, first_name=first_name,
                                        last_name=last_name)
        # create Account model
        account = Account.objects.create(user=user,
                                         username=username,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         gender=gender)
        login(request, user)
        return redirect('profile')

    return render(request, 'accounts/signup.html', context=context)


@login_required
def profile_edit_view(request):
    account = Account.objects.get(user=request.user)
    context = {
        'account': account
    }
    return render(request, 'accounts/edit_profile.html', context=context)


@require_http_methods(['POST'])
def profile_upload_image_view(request):
    uploaded_image = request.FILES.get('image_upload')

    error = check_uploaded_image(uploaded_image)
    if error:
        messages.warning(request, error, extra_tags='upload_error')
        return redirect('profile_edit')

    file_path = save_uploaded_file(uploaded_image, uploaded_image.name)
    account = Account.objects.get(user=request.user)
    account.avatar = file_path
    account.save()

    return redirect('profile_edit')


