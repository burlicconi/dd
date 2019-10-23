from django.db import models


class MonsterRace(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    features = models.CharField(max_length=5000, null=True, blank=True)
    traits = models.CharField(max_length=5000, null=True, blank=True)
    weaknesses = models.CharField(max_length=5000, null=True, blank=True)
    image_path = models.CharField(max_length=150, null=True, blank=True)
    gdrive_id = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Monster(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    race = models.ForeignKey(MonsterRace, related_name='monster_race',
                             on_delete=models.DO_NOTHING)
    subrace = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)
    special = models.CharField(max_length=5000, null=True, blank=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    sound = models.CharField(max_length=50, null=True, blank=True)
    gdrive_id = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.race)

