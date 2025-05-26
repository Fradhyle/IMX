from django.apps import apps
from django.shortcuts import render
from django.views.generic import TemplateView

from branches.forms import BranchForm


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_config = apps.get_app_config("branches")
        context["form"] = BranchForm()
        context["app_verbose_name"] = app_config.verbose_name
        return context
