from django.forms import ModelForm

from branches.models import Branch


# ModelForm for Branch app
class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = [
            "name",
            "equipment_count",
            "postcode",
            "street_address",
            "detailed_address",
            "phone_number_1",
            "phone_number_2",
        ]
