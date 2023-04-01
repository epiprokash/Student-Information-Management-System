from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
  path('login/', LoginView.as_view(), name='login'),
  path('register/', views.register_view, name='register'),
  path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
