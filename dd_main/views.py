from django.shortcuts import render
from django.views.generic import TemplateView


class StartingPage(TemplateView):
    def get(self, request):
        context = {}
        return render(request, 'starting_page.html', context)