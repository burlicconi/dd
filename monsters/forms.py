from django.forms import ModelForm, CharField, TextInput

from monsters.models import MonsterRace


class MonsterRaceForm(ModelForm):
    name = CharField(widget=TextInput(), max_length=50, error_messages={'required': 'Obavezno unesite ime!'})
    features = CharField(widget=TextInput(), max_length=5000)
    traits = CharField(widget=TextInput(), max_length=5000)
    weaknesses = CharField(widget=TextInput(), max_length=5000)
    image = CharField(widget=TextInput(), max_length=50)

    class Meta:
        model = MonsterRace
        fields = ['name', 'features', 'traits', 'weaknesses', 'image']

    def __init__(self,*args,**kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)