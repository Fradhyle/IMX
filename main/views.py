# from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "메인"

        return context
