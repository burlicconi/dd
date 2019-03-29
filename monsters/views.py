import logging

import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template import RequestContext, Context
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)

import monsters.models as models
from dd_main import settings
from gdrive_util import (handle_uploaded_file,
                         create_path_for_image,
                         download_file_from_drive)
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


def prepare_image(local_path: str, gdrive_id: str) -> str:
    """

    :param local_path: path on local storage
    :param gdrive_id: google drive id for this image
    :return: path to image file- should be always local_path; if image is not present, then download it from gdrive
    """
    if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, local_path)):
        if gdrive_id is not None:
            download_file_from_drive(file_id=gdrive_id, path=local_path)
        else:
            local_path = None
            return local_path
    return os.path.join(local_path)


class MonsterRace(CreateView):
    form_class = MonsterRaceForm
    template_name = 'monster_race.html'
    success_url = 'race'

    def get_form(self, form_class=MonsterRaceForm):
        form = super(MonsterRace, self).get_form(form_class)
        return form

    def get(self, request, pk=None):
        # find_file_in_folder('ml1')
        if pk is not None:
            monster_race = models.MonsterRace.objects.get(pk=pk)
            if monster_race.image_path is not None:
                monster_race.image_path = prepare_image(monster_race.image_path, monster_race.gdrive_id)
            form = MonsterRaceForm(instance=monster_race)
        else:
            form = MonsterRaceForm()
        return render(request, 'monster_race.html', {'form': form, 'monster_image': monster_race.image_path})

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
                    form_copy.save()
                    logger.info('Monster race successfully added to database on: '.format(path_to_save))
                    messages.add_message(request, messages.SUCCESS, 'Uspesno sacuvano!')
                    return redirect('/monsters/race/{}'.format(type_name))
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
