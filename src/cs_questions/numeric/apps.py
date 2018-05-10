from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NumericQuestionConfig(AppConfig):
    name = '....numeric'
    label = 'question_numeric'
    verbose_name = _('Numeric Questions')
