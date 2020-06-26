from django.views.generic.base import TemplateView
from django.conf import settings


class BaseAdminViews(TemplateView):

    # def get_context_data(self, **kwargs):
    #     return {"server": }

    def post(self, request):
        return self.render_to_response(self.get_context_data())