
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
from .forms import RegisterForm, VerificationForm
from .utils import send_verification_email








import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@login_required
def send_verification_email(request):
    user = request.user
    if user.email_verified:
        messages.info(request, "Ваш email уже верифицирован.")
        return redirect('main:home')

    code = str(random.randint(100000, 999999))
    user.verification_code = code
    user.save()

    send_mail(
        'Код верификации',
        f'Ваш код подтверждения: {code}',
        'accosmore@gmail.com',
        [user.email],
        fail_silently=False,
    )
    messages.success(request, "Код верификации отправлен на вашу почту.")
    return redirect('user:verify_email')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            send_verification_email(user)
            return redirect('user:verify_email')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})




def verify_email(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = request.user
            if user.verification_code == code:
                user.email_verified = True
                user.verification_code = None
                user.save()
                messages.success(request, "Email успешно верифицирован!")
                return redirect('main:home')
            else:
                messages.error(request, "Неверный код.")
    else:
        form = VerificationForm()
    return render(request, 'user/verify_email.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.email_verified:
                login(request, user)
                return redirect('products:product_list')
            else:
                return render(request, 'user/login.html', {'error': 'Подтвердите вашу почту'})
        else:
            return render(request, 'user/login.html', {'error': 'Неверные данные'})
    return render(request, 'user/login.html')


User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        username = response.data.get('username')
        user = User.objects.get(username=username)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def logout_view(request):
    logout(request)
    return redirect('user:login')