from django.shortcuts import render
from django.views.generic import TemplateView

from monsters.labels_and_desc import (race_card_desc,
                                      race_card_title,
                                      race_card_link,
                                      monster_card_desc,
                                      monster_card_title,
                                      monster_card_link
                                      )

CARD_WITH = 100
CARD_HEIGHT = 200


class StartingPage(TemplateView):
    def get(self, request):
        context = {'card': {'card_h': CARD_HEIGHT, 'card_w': CARD_WITH},
                   'race': {'desc': race_card_desc, 'title': race_card_title, 'link': race_card_link},
                   'monsters': {'desc': monster_card_desc, 'title': monster_card_title, 'link': monster_card_link}
                   }
        return render(request, 'starting_page.html', context)