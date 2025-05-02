from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from users.models import User, EmailVerification
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect, get_object_or_404


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрировались!'
    title = 'Store - Регистрация'
    
    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        return context 

class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'
    
class UserProfileView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Store - личный кабинет'
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))

class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение почты'   
    
    
    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        email = kwargs.get('email')
        user = get_object_or_404(User, email=email)
        email_verification = EmailVerification.objects.filter(user=user, code=code)

        
        if email_verification and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
        
