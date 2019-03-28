import logging
import os
import io

import pickle
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.views.generic import (ListView,
                                  CreateView)
from google_auth_httplib2 import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import monsters.models as models
from dd_main import settings
from monsters.forms import MonsterRaceForm

logger = logging.getLogger('file_info')
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FILE_ID = '1S9WtEKWr9OpJ9B2o8clIpB0jWk-DmUia'


def get_creds():
    """
    method that creates credentials for google drive API library
    :return: creds - credentials
    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('token.pickle'):
    creds = None
    if os.path.exists(os.path.join(settings.BASE_DIR, 'token.pickle')):
        with open(os.path.join(settings.BASE_DIR, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(settings.BASE_DIR, 'credentials.json'), SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(os.path.join(settings.BASE_DIR, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)
    return creds


drive_service = build('drive', 'v3', credentials=get_creds())


def create_file_meatadata_gdrive(title):
    return {'title': title}


def create_media_gdrive(filename, mimetype):
    return MediaFileUpload(filename=filename,
                           mimetype=mimetype)


def create_file_on_gdrive(file_metadata, media):
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    return file.get('id')


def create_folder_on_gdrive(name: str, parent_id: str =None) -> str:
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',

    }
    if parent_id is not None:
        file_metadata['parents'] = [parent_id]
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')


def create_folders_od_gdrive(folders_list: list, parent_id: str = None) -> str:
    """
    creates folder with name from 1st elem in list, then creates 2nd folder with 2nd name in list etc...
    :param folders_list:
    :param parent_id:
    :return:
    """
    for folder in folders_list:
        if parent_id is None:
            parent_id = create_folder_on_gdrive(folder)
        else:
            parent_id = create_folder_on_gdrive(name=folder, parent_id=parent_id)


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

    # Add file to file system
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
            logger.error('Writing image file failed: ' + str(exc))
            raise exc
    # Add file to GDrive
        create_folders_od_gdrive(folders_list=file_path.split('/')[:-1])


def download_file_from_gdrive(file_id):
    file_id = FILE_ID
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT, 'gdrive/gdrive.png'))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as exc:
            logger.error('makedirs failed: ' + str(exc))
            raise exc
    with open(os.path.join(settings.MEDIA_ROOT, 'gdrive/gdrive.png'), "wb+") as f:
        f.write(fh.getvalue())


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
        # download_file_from_gdrive('dfd')
        #metadata = create_file_meatadata_gdrive(title='Novi fajl')
        #media = create_media_gdrive(filename='/Users/burlicconi/Projects/dd/media/images/monsters/Undead22221/Undead22221.png', mimetype='image/png')
        #create_file_on_gdrive(media=media, file_metadata=metadata)
        #create_folder_on_gdrive('preko apija napravljeno!')
        create_folders_od_gdrive(['A', 'B', 'C'])
        fs = drive_service.files().list(q="name='images', mimeType= 'application/vnd.google-apps.folder'").execute()
        for f in fs:
            print(f)
        return

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
