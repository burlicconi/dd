import logging

from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)

import monsters.models as models
from gdrive_util import (handle_uploaded_file,
                         find_file_in_folder,
                         create_path_for_image)
from monsters.forms import MonsterRaceForm

logger = logging.getLogger('file_info')


def add_error_messages(request, errors):
    messages.add_message(request, messages.ERROR, 'Forma nije sacuvana!')
    for error in errors:
        logger.warning('Form had some errors')
        messages.add_message(request, messages.ERROR, errors[error][0])


def copy_form_add_update_field(request, form_class: View, field_name: str, new_value: str):
    form_copy = form_class.form_class(request.POST.copy())
    form_copy.data[field_name] = new_value
    return form_copy
    # create_path_for_image(name=type_name)


class MonsterRace(CreateView):
    form_class = MonsterRaceForm
    template_name = 'monster_race.html'
    success_url = 'race'

    def get_form(self, form_class=MonsterRaceForm):
        form = super(MonsterRace, self).get_form(form_class)
        return form

    def get(self, request, pk=None):
        #find_file_in_folder('ml1')
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
                form_copy = copy_form_add_update_field(request, self, 'image_path', path_to_save)
                if form_copy.is_valid():
                    try:
                        handle_uploaded_file(request.FILES.get('image', None), path_to_save)
                    except Exception as exc:
                        logger.error('handle_uploaded_file failed: ' + str(exc))
                        messages.add_message(request, messages.ERROR, 'Cuvanje slike nije uspelo!')
                        return render(request, 'monster_race.html')
                    monster_race = form_copy.save()
                    logger.info('Monster race successfully added to database on: '.format(path_to_save))
                    messages.add_message(request, messages.SUCCESS, 'Uspesno sacuvano!')
                    return self.get(request, type_name)
        logger.warning('Form had some errors')
        add_error_messages(request, form.errors)
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
