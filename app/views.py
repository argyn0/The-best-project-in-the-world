import django
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from .models import Todo
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin 
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import SignUpForm, TodoForm

class TodoView(ListView):
    model = Todo
    context_object_name = 'todos'
    template_name = 'home.html'

class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    success_message = 'Account created successfully'

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Verify your email'
        message = f'Hello {user.username}, please click the link below to verify your email:\n\n{verify_url}'
        send_mail(subject, message, 'sender@example.com', [user.email])

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response
    
class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = User.objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified')
            return redirect('home')
        else:
            messages.error(request, 'Invalid verification link')
            return redirect('home')
        
class Login(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    success_message = 'You are logged in successfully'

class Logout(LogoutView):
    next_page = reverse_lazy('home')

class CreateTodoView(CreateView):
    model = Todo
    form_class = TodoForm
    login_url = reverse_lazy('home')
    template_name = 'create_todo.html'
    success_url = reverse_lazy('home')

class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy('home')

class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('home')
    template_name = 'update.html'
