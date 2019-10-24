from django.forms import (ModelForm,
                          IntegerField,
                          CharField,
                          ModelChoiceField,
                          TextInput,
                          HiddenInput,
                          ImageField,
                          FileField,
                          Select,
                          NumberInput
                          )

from heroes.models import NPCHero as npchero_model
from monsters.models import MonsterRace
from util.forms_utils import create_attrs


class NPCHero(ModelForm):
    id = IntegerField(widget=HiddenInput(attrs=create_attrs('id')),
                      required=False,
                      label="id",)

    name = CharField(widget=TextInput(attrs=create_attrs('name')),
                     max_length=50,
                     error_messages={'required': 'Obavezno unesite ime!'},
                     label="Име")

    race = ModelChoiceField(widget=Select(attrs=create_attrs('race')),
                            required=False,
                            label="Раса",
                            queryset=MonsterRace.objects.all(),
                            )

    str = IntegerField(widget=NumberInput(attrs=create_attrs('str')),
                       required=True,
                       label="Снага")

    dex = IntegerField(widget=NumberInput(attrs=create_attrs('dex')),
                       required=True,
                       label="Окретност")

    con = IntegerField(widget=NumberInput(attrs=create_attrs('con')),
                       required=True,
                       label="Конституција")

    int = IntegerField(widget=NumberInput(attrs=create_attrs('int')),
                       required=True,
                       label="Интелигенција")

    wis = IntegerField(widget=NumberInput(attrs=create_attrs('wis')),
                       required=True,
                       label="Мудрост")

    cha = IntegerField(widget=NumberInput(attrs=create_attrs('cha')),
                       required=True,
                       label="Харизма")

    description = CharField(widget=TextInput(attrs=create_attrs('description')),
                            max_length=5000,
                            required=False,
                            label="Опис")

    special = CharField(widget=TextInput(attrs=create_attrs('special')),
                        max_length=5000,
                        required=False,
                        label="Специјалност")

    note = CharField(widget=TextInput(attrs=create_attrs('note')),
                     max_length=5000,
                     required=False,
                     label="Белешка")

    image_path = CharField(widget=HiddenInput(attrs=create_attrs('image_path')),
                           max_length=150,
                           required=False,
                           label="Putanja do slike",)

    gdrive_id = CharField(widget=HiddenInput(attrs=create_attrs('gdrive_id')),
                          max_length=50,
                          required=False,
                          label="GDrive ID",)

    image = ImageField(required=False,
                       label="Слика",)

    sound = FileField(required=False,
                      label="Звук",)

    class Meta:
        model = npchero_model
        fields = ['id', 'name', 'race',
                  'str', 'dex', 'con', 'int', 'wis', 'cha',
                  'description', 'special', 'note', 'image', 'image_path',
                  'sound', 'gdrive_id']
        labels = {
            'name': 'Име',
            'race': 'Раса',
            'str': 'Снага',
            'dex': 'Окретност',
            'con': 'Конституција',
            'int': 'Интелигенција',
            'wis': 'Мудрост',
            'cha': 'Харизма',
            'description': 'Опис',
            'special': 'Специјално',
            'note': 'Белешка',
            'image': 'Слика',
            'sound': 'Звук',
            'gdrive_id': 'Гдриве ид',
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)