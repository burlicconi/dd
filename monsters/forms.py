from django.forms import (ModelForm,
                          CharField,
                          TextInput,
                          ImageField,
                          HiddenInput)

from monsters.models import MonsterRace


def create_attrs(id: str) -> dict:
    return {'class': 'form_input col-sm-8 col-form-label', 'id': id + '_id'}


class MonsterRaceForm(ModelForm):
    name = CharField(widget=TextInput(attrs=create_attrs('name')),
                     max_length=50,
                     error_messages={'required': 'Obavezno unesite ime!'},
                     label="Ime")

    features = CharField(widget=TextInput(attrs=create_attrs('features')),
                         max_length=5000,
                         required=False,
                         label="Osobine")

    traits = CharField(widget=TextInput(attrs=create_attrs('traits')),
                       max_length=5000,
                       required=False,
                       label="Svojstva")

    weaknesses = CharField(widget=TextInput(attrs=create_attrs('weaknesses')),
                           max_length=5000,
                           required=False,
                           label="Slabosti")

    image_path = CharField(widget=HiddenInput(attrs=create_attrs('image_path')),
                           max_length=150,
                           required=False,
                           label="Putanja do slike",)

    gdrive_id = CharField(widget=HiddenInput(attrs=create_attrs('gdrive_id')),
                           max_length=50,
                           required=False,
                           label="GDrive ID",)

    image = ImageField(required=False,
                       label="Slika",)

    class Meta:
        model = MonsterRace
        fields = ['name', 'features', 'traits', 'weaknesses', 'image_path', 'gdrive_id']
        labels = {
            'name': 'Ime',
            'features': 'Osobine',
            'traits': 'Svojstva',
            'weaknesses': 'Slabosti',
            'image': 'Slika'
        }

    def __init__(self,*args,**kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
