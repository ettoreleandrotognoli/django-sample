from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SampleConfig(AppConfig):
    name = 'sample'
    verbose_name = _('Amostra')
