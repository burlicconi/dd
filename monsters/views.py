from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)

from monsters.forms import MonsterRaceForm


class MonsterRace(CreateView):
    form_class = MonsterRaceForm
    template_name = 'monster_race.html'
    success_url = 'success'

    def get(self, request):
        context = {}
        return render(request, 'monster_race.html', context)

    def post(self, request):
        form = get_form(self.form_class)
        if form.is_valid():
            print('valid')
            form.save()
        else:
            print('erori')
            for error in form.errors:
                messages.add_message(request, messages.ERROR, form.errors[error][0])
        context = {'message': 'caos'}
        return render(request, 'monster_race.html', context)


class MonsterRaces(ListView):

    def get(self, request):
        context = {}
        return render(request, 'monster_races.html', context)


class Monster(View):

    def get(self, request):
        context = {}
        return render(request, 'monster.html', context)


class Monsters(ListView):

    def get(self, request):
        context = {}
        return render(request, 'monsters.html', context)