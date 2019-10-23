from PIL import Image
import os.path
from io import StringIO


def thumbnail(filename, size=(50, 50), output_filename=None):
    image = Image.open(filename)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(size, Image.ANTIALIAS)

    # get the thumbnail data in memory.
    if not output_filename:
        output_filename = get_default_thumbnail_filename(filename)
    image.save(output_filename, image.format)
    return output_filename


def thumbnail_string(buf, size=(50, 50)):
    f = StringIO(buf)
    image = Image.open(f)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image = image.resize(size, Image.ANTIALIAS)
    o = StringIO()
    image.save(o, "JPEG")
    return o.getvalue()


def get_default_thumbnail_filename(filename):
    path, ext = os.path.splitext(filename)
    return path + '.thumb.jpg'


def rescale(data, width, height, force=True):
    """Rescale the given image, optionally cropping it to make sure the result image has the specified width and height."""


    max_width = width
    max_height = height

    input_file = StringIO(data)
    img = Image.open(input_file)
    if not force:
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    else:
        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 3
        img = img.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
        img = img.resize((dst_width, dst_height), Image.ANTIALIAS)

    tmp = StringIO()
    img.save(tmp, 'JPEG')
    tmp.seek(0)
    output_data = tmp.getvalue()
    input_file.close()
    tmp.close()

    return output_data
