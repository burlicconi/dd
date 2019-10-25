import logging

import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from dd_main import settings
from dd_main.parameters import THUMB_SIZE
from heroes.models import NPCHero as npc_model
from heroes.forms import NPCHeroForm
from monsters.views import copy_form_add_update_field, add_error_messages, \
    prepare_image
from util.gdrive_util import create_path_for_image, handle_uploaded_file, \
    upload_file_to_gdrive
from util.pillow_utils import thumbnail

logger = logging.getLogger('file_info')


class NPCHeroView(CreateView):
    form_class = NPCHeroForm
    template_name = 'npchero.html'
    success_url = 'npchero'

    def get_form(self, form_class=NPCHeroForm):
        form = super(NPCHeroView, self).get_form(form_class)
        return form

    def get(self, request, pk=None):
        if pk is not None:
            npchero = npc_model.objects.get(pk=pk)
            if npchero.image_path:
                npchero.image_path = prepare_image(
                    npchero.image_path,
                    npchero.gdrive_id
                )
            form = NPCHeroForm(instance=npchero)
            details = {'npchero_image': npchero.image_path,
                       'npchero_id': npchero.id
                       }
        else:  # pk is None, create Monster Race
            form = NPCHeroForm()
            details = {'monster_race_image': None, }
        return render(request, 'npchero.html', {'form': form,
                                                'details': details
                                                }
                      )

    def post(self, request, pk=None):
        # todo resiti editovanje slike i edit uopste
        if pk is not None:
            monster = npc_model.objects.get(pk=pk)
            form = NPCHeroForm(request.POST, instance=monster)
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
                    return render(request, 'npchero.html')
            saved_object = form.save()
            logger.info('Monster {} successfully updated in '
                        'database '.format(form.fields['name']))
            messages.add_message(request, messages.SUCCESS,
                                 'Uspesno sacuvano!')
            return redirect('/heroes/npchero/{}'.format(saved_object.pk))
        logger.warning('Form had some errors')
        add_error_messages(request, form.errors)
        return render(request, 'npchero.html')