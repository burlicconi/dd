from PIL import Image
import os.path

from dd_main import settings


def create_thumbnail_path(path_to_save, image_name, image_format: str):
    """
    creates path where to store thumbnail image
    :param path_to_save:
    :param image_name:
    :param image_format:
    :return:
    """
    directory = os.path.dirname(os.path.join(settings.MEDIA_ROOT,
                                             path_to_save))
    output_name = image_name + '_thumb' + image_format
    return os.path.join(directory, output_name)


def calculate_thumb_size(max_size, image_size):
    """
    calculates max size of thumbnail image to avoid deformations
    :param max_size: max size of thumbnail
    :param image_size: original image size
    :return: size of thumbnail image
    """
    if image_size[0] < max_size[0] and image_size[1] < max_size[1]:
        return image_size
    ratio_width = image_size[0]/max_size[0]
    ratio_heigh = image_size[1]/max_size[1]
    if ratio_width > ratio_heigh:
        w = max_size[0]
        h = image_size[1] / ratio_width
    else:
        h = max_size[1]
        w = image_size[0] / ratio_heigh
    return int(w), int(h)


def thumbnail(path_to_save, image_name, max_size):
    """
    creates thumbnail from image
    :param path_to_save:  path where to save thumbnail and where original
        image is
    :param image_name: name of original image
    :param max_size: max size for thumbnail - if original image is larger,
    it will be cut to fit max size w/o deformations
    :return: path of thumbnail image
    """
    full_path = os.path.join(settings.MEDIA_ROOT, path_to_save)
    image = Image.open(full_path)
    output_path = create_thumbnail_path(path_to_save,
                                        image_name,
                                        full_path[full_path.index('.'):])
    thumb_size = calculate_thumb_size(max_size, image.size)

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(thumb_size, Image.ANTIALIAS)

    # get the thumbnail data in memory.
    image.save(output_path, quality=95)
    relative_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
    return relative_path


size = calculate_thumb_size((300, 150), (600, 1500))
print(size)
