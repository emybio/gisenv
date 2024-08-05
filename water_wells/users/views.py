from django.contrib.auth.views import LoginView
from django.shortcuts import redirect,render
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def index(request):
    return render(request,'users/index.html')



User = get_user_model()
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            return redirect('register')
        return super().form_valid(form)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Kullanıcıyı hemen aktif yapma
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def notify_admin_of_new_user(user):
    subject = 'Yeni Kullanıcı Kaydı'
    message = f'Yeni kullanıcı kaydı: {user.username}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['emrah0denizer.gmail.com']  # Yönetici e-posta adresi
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')


@staff_member_required
def approve_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users_list')  # Yönlendirmek istediğiniz URL

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')