from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView

from accounts.models import Account
from django.contrib.auth.decorators import login_required
from .utils import save_uploaded_file, check_uploaded_image, validate_name, validate_username


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
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def signup_view(request):
    context = {}

    if request.method == 'POST':

        first_name = request.POST.get('firstname').strip()
        last_name = request.POST.get('lastname').strip()
        gender = request.POST.get('gender').strip()
        age = request.POST.get('age').strip()
        username = request.POST.get('login').strip().lower()
        email = request.POST.get('email').strip().lower()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'username': username,
            'email': email
        }

        # check firstname and lastname
        if not first_name or not last_name or not validate_name(first_name) or not validate_name(last_name):
            messages.warning(request, 'Имя и фамилия должны состоять только из русских или латинских букв')
            return render(request, 'accounts/signup.html', context=context)

        # check username
        if not username or not validate_username(username):
            messages.warning(request, 'Логин должен состоять только из латинских букв, цифр или символа подчеркивания')
            return render(request, 'accounts/signup.html', context=context)

        # check unique username
        if username and User.objects.filter(username=username).exists():
            messages.warning(request, f'Логин {username} уже занят')
            return render(request, 'accounts/signup.html', context=context)

        # validate email
        try:
            validate_email(email)
        except ValidationError as error:
            for e in error.messages:
                messages.error(request, e)
            return render(request, 'accounts/signup.html', context=context)

        # check unique email
        if email and User.objects.filter(email=email).exists():
            messages.warning(request, 'Такой email уже зарегистрирован')
            return render(request, 'accounts/signup.html', context=context)

        # check age
        if age:
            try:
                age = abs(int(age))
            except ValueError:
                messages.warning(request, 'Возраст должен состоять из цифр')
                return render(request, 'accounts/signup.html', context=context)
        else:
            age = None

        # check equals passwords
        if not password1 or not password2 or password1 != password2:
            messages.warning(request, 'Пароли не совпадают')
            return render(request, 'accounts/signup.html', context=context)

        # validate password
        try:
            validate_password(password1)
        except ValidationError as error:
            for e in error:
                messages.warning(request, e)
            return render(request, 'accounts/signup.html', context=context)

        # gender to int
        if gender == 'male':
            gender = 1
        else:
            gender = 0

        # create User model
        user = User.objects.create_user(username=username, email=email, password=password2, first_name=first_name,
                                        last_name=last_name)
        # create Account model
        Account.objects.create(user=user,
                               username=username,
                               first_name=first_name,
                               last_name=last_name,
                               age=age,
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


@login_required
@require_http_methods(['POST'])
def profile_upload_image(request):
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


@login_required
@require_http_methods(['POST'])
def update_profile(request):
    account = Account.objects.get(user=request.user)

    data = {
        'status': request.POST.get('status'),
        'first_name': request.POST.get('firstname').strip(),
        'last_name': request.POST.get('lastname').strip(),
        'email': request.POST.get('email').lower().strip(),
        'gender': request.POST.get('gender').strip(),
        'age': request.POST.get('age').strip(),
        'city': request.POST.get('city').strip(),
        'job': request.POST.get('job').strip(),
        'about': request.POST.get('about').strip()
    }

    if (not data.get('first_name')
            or not data.get('last_name')
            or not validate_name(data.get('first_name'))
            or not validate_name(data.get('last_name'))):
        messages.warning(request, 'Имя и фамилия должны состоять из русских или латинских букв')
        return redirect('profile_edit')

    # validate email
    try:
        validate_email(data['email'])
    except ValidationError as error:
        for e in error.messages:
            messages.error(request, e)
        return redirect('profile_edit')

    # check exists email
    if (data['email'] != account.email
            and Account.objects.filter(email=data.get('email')).exists()):
        messages.warning(request, 'Такой email уже зарегистрирован')
        return redirect('profile_edit')

    # check age
    if data.get('age'):
        try:
            data['age'] = abs(int(data['age']))
        except ValueError:
            messages.warning(request, 'Возраст должен состоять из цифр')
            return redirect('profile_edit')
    else:
        data['age'] = None

    # normalize gender
    if data['gender'] == 'male':
        data['gender'] = 1
    else:
        data['gender'] = 0

    # update account attrs
    for key, value in data.items():
        setattr(account, key, value)

    account.save()
    return redirect('profile')


@login_required
def change_password_view(request):
    account = Account.objects.get(user=request.user)
    context = {'account': account}
    return render(request, 'accounts/change_password.html', context)


@login_required
@require_http_methods(['POST'])
def update_password(request):
    user = request.user

    old_password = request.POST.get('oldpassword')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # check old password
    if not old_password or not user.check_password(old_password):
        messages.warning(request, 'Старый пароль неверный')
        return redirect('profile_change_password')

    # check equals new password
    if not password1 or not password2 or password1 != password2:
        messages.warning(request, 'Пароли не совпадают')
        return redirect('profile_change_password')

    # check new password
    try:
        validate_password(password1)
    except ValidationError as error:
        for e in error:
            messages.warning(request, e)
        return redirect('profile_change_password')

    user.set_password(password1)
    messages.success(request, 'Пароль успешно изменен', extra_tags='pwd_changed')

    return redirect('profile_edit')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/user_profile.html'
    context_object_name = 'account'
    slug_field = 'username'


class PeopleView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/people.html'
    context_object_name = 'accounts'
    paginate_by = 20
