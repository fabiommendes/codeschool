from codeschool import panels
from django.utils.text import ugettext_lazy as _

from src.questions.base.admin import QuestionAdmin
from . import models


class CodeQuestionAdmin(QuestionAdmin):

    class Meta:
        model = models.CodeQuestion

    content_panels = [
        ...,

        panels.MultiFieldPanel([
            panels.FieldPanel('grader'),
            panels.FieldPanel('reference'),
            panels.FieldPanel('function_name'),
            panels.FieldPanel('timeout'),
        ], heading=_('Options')),
    ]
