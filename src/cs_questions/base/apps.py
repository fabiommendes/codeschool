from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class QuestionsConfig(AppConfig):
    name = '....base'
    label = 'questions'
    verbose_name = _('Questions')
