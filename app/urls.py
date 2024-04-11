from django.contrib import admin
from django.urls import path
from .views import TodoView, SignUpView, VerifyEmailView, Login, Logout, CreateTodoView, TodoDeleteView, TodoUpdateView

urlpatterns = [
    path('', TodoView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create_todo/', CreateTodoView.as_view(), name='create_todo'),
    path('delete/<int:pk>/',TodoDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/',TodoUpdateView.as_view(), name='update'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='verify'),
]
