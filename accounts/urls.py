from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', views.register_view, name='register'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('login/', views.LoginView().as_view(), name='user_login'),
    path('create_account/', views.RegisterView().as_view(), name='create_account'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
