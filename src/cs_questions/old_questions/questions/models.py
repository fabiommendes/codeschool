from boogie.extensible import extensible
from django import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField

QUESTION_BODY_BLOCKS = [
    ('paragraph', blocks.RichTextBlock()),
    ('heading', blocks.CharBlock(classname='full title')),
    ('markdown', MarkdownBlock()),
    ('html', blocks.RawHTMLBlock()),
]


class Question(*extensible('questions.Question', models.Model)):
    """
    Base abstract class for all question types.
    """

    class Meta:
        abstract = True
        permissions = (("download_question", "Can download question files"),)

    body = StreamField(
        QUESTION_BODY_BLOCKS,
        blank=True,
        null=True,
        verbose_name=_('Question description'),
        help_text=_(
            'Describe what the question is asking and how should the students '
            'answer it as clearly as possible. Good questions should not be '
            'ambiguous.'
        ),
    )
    comments = RichTextField(
        _('Comments'),
        blank=True,
        help_text=_('(Optional) Any private information that you want to '
                    'associate to the question page.')
    )
    import_file = models.FileField(
        _('import question'),
        null=True,
        blank=True,
        upload_to='question-imports',
        help_text=_(
            'Fill missing fields from question file. You can safely leave this '
            'blank and manually insert all question fields.'
        )
    )


class QuestionMixin:
    """
    Shared properties for submissions, progress and feedback models.
    """
    question = property(lambda x: x.activity)
    question_id = property(lambda x: x.activity_id)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        if question is not None:
            kwargs.setdefault('activity', question)
        super().__init__(*args, **kwargs)


class QuestionSubmission(QuestionMixin, Submission):
    """
    Abstract class for submissions to questions.
    """

    class Meta:
        abstract = True


class QuestionProgress(QuestionMixin, Progress):
    """
    Abstract class for keeping up with the progress of student responses.
    """

    class Meta:
        abstract = True


class QuestionFeedback(QuestionMixin, Feedback):
    """
    Abstract class for representing feedback to users.
    """

    class Meta:
        abstract = True
