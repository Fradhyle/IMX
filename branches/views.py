from django.apps import apps
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


class CreateBranchView(TemplateView):
    template_name = "create_branch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_config = apps.get_app_config("branches")
        context["form"] = BranchForm()
        context["app_verbose_name"] = app_config.verbose_name

        return context


class ShowBranchView(TemplateView):
    template_name = "show_branch.html"

    def get_context_data(self, **kwargs):
        app_config = apps.get_app_config("branches")

        context = super().get_context_data(**kwargs)
        context["app_verbose_name"] = app_config.verbose_name

        serial = kwargs.get("serial")

        Branch = apps.get_model("branches", "Branch")
        branch = Branch.objects.filter(serial=serial).first()
        if branch:
            context["branch"] = branch
        else:
            context["error"] = "Branch not found"

        return context
