"""monsters URL Configuration

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

from django.urls import path

from .views import (Monster,
                    Monsters,
                    MonsterRace,
                    MonsterRaces)

urlpatterns = [
    # Monsters
    path(r'', Monsters.as_view(), name='monsters'),
    path(r'monster', Monster.as_view(), name='monster'),
    path('monster/<str:pk>', Monster.as_view(), name='monster'),

    # Monster race
    path(r'races', MonsterRaces.as_view(), name='races'),
    path(r'race', MonsterRace.as_view(), name='race'),
    path('race/<str:pk>', MonsterRace.as_view(), name='race'),
]
