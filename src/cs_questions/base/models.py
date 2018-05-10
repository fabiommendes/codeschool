from django.utils.translation import ugettext_lazy as _

from boogie import models
from cs_lms.activities.models import Submission, Progress
from cs_lms.activities.models.feedback import Feedback


class Question(models.Model):
    """
    Base abstract class for all question types.
    """

    name = models.NameField()
    short_description = models.ShortDescriptionField()
    description = models.LongDescriptionField(
        help_text=_(
            'Describe what the question is asking and how should the students '
            'answer it as clearly as possible. Good questions should not be '
            'ambiguous.'
        ),
    )
    comments = models.TextField(
        _('Comments'),
        blank=True,
        help_text=_(
            'Arbitrary private information that you want to associate to the '
            'question page. This data is only available to the question '
            'author and staff members.'
        )
    )

    class Meta:
        abstract = True
        permissions = [
            ("download_question", "Can download question files"),
        ]


class QuestionMixin:
    """
    Shared properties for submissions, progress and feedback models.
    """

    question = property(lambda x: x.activity)
    question_id = property(lambda x: x.activity_id)


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


# Update the Question._meta attribute
Question._meta.submission_class = QuestionSubmission
Question._meta.progress_class = QuestionProgress
Question._meta.feedback_class = QuestionFeedback
