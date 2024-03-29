"""dd_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from dd_main.views import StartingPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('monsters/', include('monsters.urls')),
    path('heroes/', include('heroes.urls')),
    path('', auth_views.LoginView.as_view(template_name='login.html')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('starting_page/', StartingPage.as_view(), name='starting_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
