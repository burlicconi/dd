import logging
import os
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)

import monsters.models as models
from dd_main import settings
from monsters.forms import MonsterRaceForm

logger = logging.getLogger('file_info')


def create_path_for_image(type: str = None, name: str = None) -> str:
    base_path = 'monsters'
    try:
        if type is None:
            return os.path.join('images', base_path, str(name), str(name)) + '.png'
        else:
            return os.path.join('images', base_path, str(type)) + '.png'
    except Exception as exc:
        logger.error('creating path for moster image failed: ' + str(exc))
        raise exc


def handle_uploaded_file(file, file_path: str):
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT, file_path))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as exc:
            logger.error('makedirs failed: ' + str(exc))
            raise exc
    with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as destination:
        try:
            for chunk in file.chunks():
                destination.write(chunk)
        except Exception as exc:
            logger.error('Writting image file failed: ' + str(exc))
            raise exc


class MonsterRace(CreateView):
    form_class = MonsterRaceForm
    template_name = 'monster_race.html'
    success_url = 'race'

    def get_form(self, form_class=MonsterRaceForm):
        form = super(MonsterRace, self).get_form(form_class)
        return form

    def get(self, request, pk=None):
        if pk is not None:
            monster_race = models.MonsterRace.objects.get(pk=pk)
            form = MonsterRaceForm(monster_race)
        else:
            form = MonsterRaceForm()
        return render(request, 'monster_race.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            type_name = request.POST.get('name', None)
            if type_name is not None:
                path_to_save = create_path_for_image(name=type_name)
                form_copy = self.form_class(request.POST.copy())
                form_copy.data['image_path'] = path_to_save
                image_file = request.FILES['image']
                if form_copy.is_valid():
                    try:
                        handle_uploaded_file(image_file, path_to_save)
                    except Exception as exc:
                        logger.error('handle_uploaded_file failed: ' + str(exc))
                        messages.add_message(request, messages.ERROR, 'Cuvanje slike nije uspelo!')
                        return render(request, 'monster_race.html')
                    monster_race = form_copy.save()
                    logger.info('Monster race successfully added to database on: '.format(path_to_save))
                    messages.add_message(request, messages.SUCCESS, 'Uspesno sacuvano!')
                    self.get(request, monster_race.pk)
        logger.warning('Form had some errors')
        messages.add_message(request, messages.ERROR, 'Forma nije sacuvana!')
        for error in form.errors:
            logger.warning('Form had some errors')
            messages.add_message(request, messages.ERROR, form.errors[error][0])
        return render(request, 'monster_race.html')


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