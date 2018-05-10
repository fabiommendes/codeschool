from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FilesConfig(AppConfig):
    name = 'codeschool.core.files'
    verbose_name = _('Files types and programming languages.')
