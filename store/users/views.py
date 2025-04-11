from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from users.models import User


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    
    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        return context 

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                form.add_error(None, "Неверный логин или пароль")  # Сообщение об ошибке
    else:
        form = UserLoginForm()
    
    context = {'form': form}
    return render(request, 'users/login.html', context)

class UserProfileUpdateView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user = self.object)
        return context

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


    



# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else: 
#         form = UserRegistrationForm()
#     context = {'form' : form}
#     return render(request, 'users/registration.html', context)

# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance= request.user, data = request.POST, files=request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             if 'image' in request.FILES:  # Проверяем, есть ли файл
#                 user.image = request.FILES['image']  # Принудительно добавляем
#             user.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)

#     context = {
#         'title': 'Store - Профиль', 
#         'form': form,
#         'baskets': Basket.objects.filter(user = request.user)
#         }
#     return render(request, 'users/profile.html', context)
