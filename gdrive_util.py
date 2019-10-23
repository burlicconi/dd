import logging
import os
import io

import pickle

from google_auth_httplib2 import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from dd_main import settings

logger = logging.getLogger('file_info')
SCOPES = ['https://www.googleapis.com/auth/drive.file']
BASE_PATH_MONSTERS = 'monsters'


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


def create_file_metadata_gdrive(title):
    return {'title': title}


def create_media_gdrive(filename, mimetype):
    return MediaFileUpload(filename=filename,
                           mimetype=mimetype)


def create_file_on_gdrive(file_path: str, parent_ids: list):
    """

    :param file_path: path to file on local storage
    :param parent_ids: ids of parents folders on gdrive
    :return: id of newly inserted file on gdrive
    """
    try:
        file_metadata = {'name': file_path.split('/')[-1],
                         'parents': [parent_ids[-1]]
                         }
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        media = MediaFileUpload(full_file_path,
                                mimetype='image/jpeg',
                                resumable=True)

        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        return file.get('id')
    except Exception as exc:
        logger.error('inserting image on GDrive failed: ' + str(exc))


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
    creates folder with name from 1st elem in list,
        then creates 2nd folder with 2nd name in list etc...
    :param folders_list:
    :param parent_id:
    :return:
    """
    created_folders_ids = []
    for folder in folders_list:
        if parent_id is None:
            parent_id = create_folder_on_gdrive(folder)
        else:
            parent_id = create_folder_on_gdrive(name=folder,
                                                parent_id=parent_id)
        created_folders_ids.append(parent_id)
    return created_folders_ids


def retrieve_or_create_folders_od_gdrive(folders_list: list,
                                         parent_id: str = None) -> str:
    """
    :param folders_list: list of nested folders that either should be retrieved
        or created if they don't exist
    :param parent_id: parent folder for this list of folders
    :return:
    """
    if len(folders_list) > 0:
        ids = []
        if parent_id is None:
            parent_id = 'root'
        folder_id = find_folder_in_parent_folder(folders_list[0], parent_id)
        if folder_id is None:
            # if folder does not exist, create new folder in parent folder
            folder_id = create_folder_on_gdrive(folders_list[0], parent_id)
        ids.append(folder_id)
        if len(folders_list) > 1:
            for i in range (1, len(folders_list)):
                folder_id = find_folder_in_parent_folder(folders_list[i],
                                                         ids[-1])
                if folder_id is None:
                    # if folder does not exist,
                    # create new folder in parent folder
                    folder_id = create_folder_on_gdrive(folders_list[i],
                                                        ids[-1])
                ids.append(folder_id)
        return ids


def create_path_for_image(type: str = None, name: str = None) -> str:
    try:
        if type is None:
            return os.path.join('images',
                                BASE_PATH_MONSTERS,
                                str(name),
                                str(name)) + '.png'
        else:
            return os.path.join('images',
                                BASE_PATH_MONSTERS,
                                str(type)) + '.png'
    except Exception as exc:
        logger.error('creating path for moster image failed: ' + str(exc))
        raise exc


def handle_uploaded_file(file, file_path: str):
    """
    saves uploaded file to file system and then uploads file to gdrive
    :param file:
    :param file_path:
    :return:
    """
    if file is None:
        return
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT, file_path))

    # Add file to file system
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as exc:
            logger.error('makedirs failed: ' + str(exc))
            raise exc
    with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as dest:
        try:
            for chunk in file.chunks():
                dest.write(chunk)
        except Exception as exc:
            logger.error('Writing image file failed: ' + str(exc))
            raise exc
        # Add file to GDrive
        created_folders_ids = retrieve_or_create_folders_od_gdrive(
            folders_list=file_path.split('/')[:-1]
        )
        create_file_on_gdrive(file_path, created_folders_ids)


def find_folder_by_name(name: str) -> str:
    """

    :param name: folder name to search
    :return: folder id
    """
    try:
        result = drive_service.files().list(
            q='name="{}" and mimeType = "application/vnd.google-apps.folder"'
              ''.format(name)).execute()
        return result['files'][0]['id']
    except Exception as exc:
        logger.error('Could not find folder on GDrive with name {}'
                     ' '.format(name)+ '; ' + str(exc))
        return None


def find_file_in_folder(name: str) -> str:
    folder_id = find_folder_by_name(name)
    result = drive_service.files().list(q='"{}" in parents'.format(folder_id)).execute()
    return result['files'][0]['id']


def find_folder_in_parent_folder(folder_name: str, parent_name: str) -> str:
    folder_id = find_folder_by_name(parent_name)
    if folder_id is not None:
        result = drive_service.files().list(q='name = "{}" and "{}" in parents'
                                              ''.format(
                                                    folder_name,
                                                    folder_id)
                                                ).execute()
    else:
        result = drive_service.files().list(q='name = "{}"'
                                              ''.format(folder_name)).execute()
    if len(result['files']) > 0:
        return result['files'][0]['id']
    else:
        return None


def download_file_from_drive(name: str, path: str):
    """

    :param name: folder name on gdrive
    :param path: path where to save on local storage
    :return:
    """
    file_id = find_file_in_folder(name)
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    logger.info('Downloaded file from gdrive with ID = {}'.format(file_id))
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT, path))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as exc:
            logger.error('makedirs failed: ' + str(exc))
            raise exc
    with open(os.path.join(settings.MEDIA_ROOT,
                           'gdrive/gdrive.png'),
              "wb+") as f:
        try:
            f.write(fh.getvalue())
        except Exception as exc:
            logger.error('Writing file from gdrive failed ' + str(exc))
            raise exc
    return True


def download_file_from_drive(file_id: str, path: str):
    """

    :param file_id: ID of file on gdrive
    :param path: path where to save on local storage
    :return:
    """
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    logger.info('Downloaded file from gdrive with ID = {}'.format(file_id))
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT, path))
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as exc:
            logger.error('makedirs failed: ' + str(exc))
            raise exc
    with open(os.path.join(settings.MEDIA_ROOT,
                           'gdrive/gdrive.png'),
              "wb+") as f:
        try:
            f.write(fh.getvalue())
        except Exception as exc:
            logger.error('Writing file from gdrive failed ' + str(exc))
            raise exc
    return True
