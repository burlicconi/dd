import logging

import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)

from dd_main.parameters import THUMB_SIZE
from monsters.models import (MonsterRace as races_model,
                             Monster as monsters_model)
from dd_main import settings
from gdrive_util import (handle_uploaded_file,
                         create_path_for_image,
                         download_file_from_drive, upload_file_to_gdrive)
from pillow_utils import thumbnail
from monsters.forms import MonsterRaceForm, MonsterForm

logger = logging.getLogger('file_info')


def add_error_messages(request, errors):
    messages.add_message(request, messages.ERROR, 'Forma nije sacuvana!')
    for error in errors:
        logger.warning('Form had some errors')
        messages.add_message(request, messages.ERROR, errors[error][0])


def copy_form_add_update_field(request, form_class: View,
                               field_name: str, new_value: str):
    form_copy = form_class.form_class(request.POST.copy())
    form_copy.data[field_name] = new_value
    return form_copy


def prepare_image(local_path: str, gdrive_id: str) -> str:
    """

    :param local_path: path on local storage
    :param gdrive_id: google drive id for this image
    :return: path to image file- should be always local_path; if image
    is not present, then download it from gdrive
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
        if pk is not None:
            monster_race = races_model.objects.get(pk=pk)
            if monster_race.image_path:
                monster_race.image_path = prepare_image(
                    monster_race.image_path,
                    monster_race.gdrive_id
                )
            form = MonsterRaceForm(instance=monster_race)
            details = {'monster_race_image': monster_race.image_path,
                       'monster_id': monster_race.id
                       }
        else:  # pk is None, create Monster Race
            form = MonsterRaceForm()
            details = {'monster_race_image': None, }
        return render(request, 'monster_race.html', {'form': form,
                                                     'details': details
                                                     }
                      )

    def post(self, request, pk=None):
        if pk is not None:
            race = races_model.objects.get(pk=pk)
            form = MonsterRaceForm(request.POST, instance=race)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            type_name = request.POST.get('name', None)
            if type_name is not None:
                path_to_save = create_path_for_image(name=type_name)
            if form.is_valid():
                try:
                    handle_uploaded_file(request.FILES.get('image', None),
                                         path_to_save)
                    thumb = thumbnail(path_to_save=path_to_save,
                                      image_name=type_name,
                                      max_size=THUMB_SIZE)
                    form = copy_form_add_update_field(request,
                                                      self,
                                                      'image_path',
                                                      thumb)
                    upload_file_to_gdrive(thumb)
                    # remove original image, save thumbnail
                    os.remove(os.path.join(settings.MEDIA_ROOT, path_to_save))
                except Exception as exc:
                    logger.error('handle_uploaded_file failed: ' + str(exc))
                    messages.add_message(request, messages.ERROR,
                                         'Cuvanje slike nije uspelo!')
                    return render(request, 'monster_race.html')
                saved_object = form.save()
                logger.info('Monster race {} successfully updated in '
                            'database '.format(form.fields['name']))
                messages.add_message(request, messages.SUCCESS,
                                     'Uspesno sacuvano!')
                return redirect('/monsters/race/{}'.format(saved_object.pk))
        logger.warning('Form had some errors')
        add_error_messages(request, form.errors)
        return render(request, 'monster_race.html')


class MonsterRaces(ListView):
    def get(self, request):
        all = races_model.objects.all()
        context = {'all': all}
        return render(request, 'monster_races.html', context)


class Monster(View):
    form_class = MonsterForm
    template_name = 'monster.html'
    success_url = 'monster'

    def get_form(self, form_class=MonsterForm):
        form = super(Monster, self).get_form(form_class)
        return form

    def get(self, request, pk=None):
        if pk is not None:
            monster = monsters_model.objects.get(pk=pk)
            if monster.image_path:
                monster.image_path = prepare_image(
                    monster.image_path,
                    monster.gdrive_id
                )
            form = MonsterForm(instance=monster)
            details = {'monster_image': monster.image_path,
                       'monster_id': monster.id}
        else:  # pk is None, create Monster Race
            form = MonsterForm()
            details = {'monster_image': None, }
        return render(request, 'monster.html', {'form': form,
                                                'details': details,
                                                }
                      )

    def post(self, request, pk=None):
        # todo resiti editovanje slike i edit uopste
        if pk is not None:
            monster = monsters_model.objects.get(pk=pk)
            form = MonsterForm(request.POST, instance=monster)
        else:
            form = self.form_class(request.POST)
        if form.is_valid():
            type_name = request.POST.get('name', None)
            image = request.POST.get('image', None)
            if image is not '':
                try:
                    if type_name is not None:
                        path_to_save = create_path_for_image(name=type_name)
                    handle_uploaded_file(request.FILES.get('image', None),
                                         path_to_save)
                    thumb = thumbnail(path_to_save=path_to_save,
                                      image_name=type_name,
                                      max_size=THUMB_SIZE)
                    form = copy_form_add_update_field(request,
                                                      self,
                                                      'image_path',
                                                      thumb)
                    upload_file_to_gdrive(thumb)
                    # remove original image, save thumbnail
                    os.remove(os.path.join(settings.MEDIA_ROOT, path_to_save))
                except Exception as exc:
                    logger.error('handle_uploaded_file failed: ' + str(exc))
                    messages.add_message(request, messages.ERROR,
                                         'Cuvanje slike nije uspelo!')
                    return render(request, 'monster.html')
            saved_object = form.save()
            logger.info('Monster {} successfully updated in '
                        'database '.format(form.fields['name']))
            messages.add_message(request, messages.SUCCESS,
                                 'Uspesno sacuvano!')
            return redirect('/monsters/monster/{}'.format(saved_object.pk))
        logger.warning('Form had some errors')
        add_error_messages(request, form.errors)
        return render(request, 'monster.html')


class Monsters(ListView):
    def get(self, request):
        all = monsters_model.objects.all()
        context = {'all': all}
        return render(request, 'monsters.html', context)
