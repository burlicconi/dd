from django.urls import path

from heroes.views import NPCHeroView

urlpatterns = [
    # Heroes
    #path(r'', NPCHeroView.as_view(), name='npchero'),
    path(r'npchero', NPCHeroView.as_view(), name='npchero'),
    path('npchero/<str:pk>', NPCHeroView.as_view(), name='npchero'),
]
