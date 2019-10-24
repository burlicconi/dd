from django.db import models

from monsters.models import MonsterRace


class NPCHero(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    race = models.ForeignKey(MonsterRace, related_name='npc_hero_monster_race',
                             on_delete=models.DO_NOTHING)
    str = models.PositiveSmallIntegerField(null=False)
    dex = models.PositiveSmallIntegerField(null=False)
    con = models.PositiveSmallIntegerField(null=False)
    int = models.PositiveSmallIntegerField(null=False)
    wis = models.PositiveSmallIntegerField(null=False)
    cha = models.PositiveSmallIntegerField(null=False)

    description = models.CharField(max_length=5000, null=True, blank=True)
    special = models.CharField(max_length=5000, null=True, blank=True)
    note = models.CharField(max_length=5000, null=True, blank=True)
    image = models.CharField(max_length=50, null=True, blank=True)
    image_path = models.CharField(max_length=150, null=True, blank=True)
    sound = models.CharField(max_length=50, null=True, blank=True)
    gdrive_id = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.race)

    def __str__(self):
        return '{}, раса {}'.format(self.name, self.race)