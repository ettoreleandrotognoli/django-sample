from . import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory


class MovementForm(ModelForm):
    class Meta:
        model = models.Movement

MovementAnnexFormSet = inlineformset_factory()