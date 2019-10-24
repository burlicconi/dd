from django.forms import (ModelForm,
                          CharField,
                          TextInput,
                          ImageField,
                          HiddenInput, IntegerField, FileField, ChoiceField,
                          Select, ModelChoiceField)

from monsters.models import MonsterRace, Monster


def create_attrs(id: str) -> dict:
    return {'class': 'form_input col-sm-8 col-form-label', 'id': id + '_id'}


def all_races():
    races = MonsterRace.objects.all()
    races_tuple = []
    for race in races:
        races_tuple.append((race.id, race.name))
    return races_tuple


class MonsterRaceForm(ModelForm):
    id = IntegerField(widget=HiddenInput(attrs=create_attrs('id')),
                           required=False,
                           label="id",)

    name = CharField(widget=TextInput(attrs=create_attrs('name')),
                     max_length=50,
                     error_messages={'required': 'Obavezno unesite ime!'},
                     label="Име")

    features = CharField(widget=TextInput(attrs=create_attrs('features')),
                         max_length=5000,
                         required=False,
                         label="Особине")

    traits = CharField(widget=TextInput(attrs=create_attrs('traits')),
                       max_length=5000,
                       required=False,
                       label="Својства")

    weaknesses = CharField(widget=TextInput(attrs=create_attrs('weaknesses')),
                           max_length=5000,
                           required=False,
                           label="Слабости")

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

    class Meta:
        model = MonsterRace
        fields = ['id', 'name', 'features', 'traits', 'weaknesses',
                  'image_path', 'gdrive_id']
        labels = {
            'name': 'Име',
            'features': 'Особине',
            'traits': 'Својства',
            'weaknesses': 'Слабости',
            'image': 'Слика'
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class MonsterForm(ModelForm):
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

    subrace = CharField(widget=TextInput(attrs=create_attrs('subrace')),
                       max_length=50,
                       required=False,
                       label="Подраса")

    description = CharField(widget=TextInput(attrs=create_attrs('description')),
                           max_length=5000,
                           required=False,
                           label="Опис")

    special = CharField(widget=TextInput(attrs=create_attrs('special')),
                            max_length=5000,
                            required=False,
                            label="Специјално")

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
        model = Monster
        fields = ['id', 'name', 'race', 'subrace', 'description',
                  'special', 'note', 'image', 'image_path', 'sound',
                  'gdrive_id']
        labels = {
            'name': 'Име',
            'race': 'Раса',
            'subrace': 'Подраса',
            'description': 'Опис',
            'special': 'Специјално',
            'note': 'Белешка',
            'image': 'Слика',
            'sound': 'Звук',
            'gdrive_id': 'Гдриве ид',
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)