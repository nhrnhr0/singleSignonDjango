"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import register_screen, get_screen_access, get_standalog_server_url,get_user_info
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('api/get-user-info/', get_user_info, name='get_user_info'),
    
    path('register-screen/', register_screen, name='register_screen'),
    path('get-screen-access/', get_screen_access, name='get_screen_access'),
    path('get-standalog-server-url/', get_standalog_server_url, name='get_standalog_server_url'),
    
]
