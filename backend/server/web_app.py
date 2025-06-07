from django.views import View
from django.http import HttpResponse, Http404

import os


class ReactAppView(View):
    def get(self, request, *args, **kwargs):
        try:
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            raise Http404("React build not found")