from . import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory


class MovementForm(ModelForm):
    class Meta:
        model = models.Movement
        fields = '__all__'

MovementAnnexFormSet = inlineformset_factory(models.Movement,models.MovementAnnex,fields='__all__',extra=1)