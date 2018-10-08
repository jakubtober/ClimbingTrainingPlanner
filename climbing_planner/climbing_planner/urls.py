"""climbing_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from planner_app.views import (
    WelcomeView,
    LoginView,
    LogoutView,
    RegisterView,
    ActivateUserView,
    ResetPasswordView,
    SetNewPasswordView,
    HomeView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/activate$', ActivateUserView.as_view(), name='activate-user'),
    url(r'^reset-password/$', ResetPasswordView.as_view(), name='reset-password'),
    url(r'^set-new-password$', SetNewPasswordView.as_view(), name='set-new-password'),
    url(r'^home/$', HomeView.as_view(), name='home'),
]
