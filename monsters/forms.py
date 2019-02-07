from django.forms import ModelForm, CharField, TextInput

from monsters.models import MonsterRace


class MonsterRaceForm(ModelForm):
    name = CharField(widget=TextInput(), max_length=50, error_messages={'required': 'Obavezno unesite ime!'})
    features = CharField(widget=TextInput(), max_length=5000, required=False)
    traits = CharField(widget=TextInput(), max_length=5000, required=False)
    weaknesses = CharField(widget=TextInput(), max_length=5000, required=False)
    image = CharField(widget=TextInput(), max_length=50, required=False)

    class Meta:
        model = MonsterRace
        fields = ['name', 'features', 'traits', 'weaknesses', 'image']

    def __init__(self,*args,**kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
