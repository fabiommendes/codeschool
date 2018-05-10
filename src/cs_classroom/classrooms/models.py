from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from boogie import models
from boogie.fields import IntEnum
from boogie.rest import rest_api
from boogie.utils.phrases import phrase_lower
from .managers import ClassroomManager
from .mixins import DescriptiveModel

User = get_user_model()


class CommentPolicyEnum(IntEnum):
    NONE = 0, _('Only teachers can post and comment')
    COMMENT = 1, _('Students can comment, but not post')
    POST_AND_COMMENT = 2, _('Everyone can post and comment')


@rest_api
class Classroom(DescriptiveModel):
    """
    One specific occurrence of a course for a given teacher in a given period.
    """

    long_description = models.LongDescriptionField(blank=True)
    discipline = models.ForeignKey(
        'Discipline',
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    location = models.CharField(
        _('location'),
        blank=True,
        max_length=140,
        help_text=_('Physical location of classroom, if applicable.'),
    )
    teacher = models.ForeignKey(
        User,
        related_name='classrooms_as_teacher',
        on_delete=models.PROTECT
    )
    students = models.ManyToManyField(
        User,
        verbose_name=_('students'),
        related_name='classrooms_as_student',
        blank=True,
    )
    staff = models.ManyToManyField(
        User,
        verbose_name=_('staff'),
        related_name='classrooms_as_staff',
        blank=True,
    )
    is_accepting_subscriptions = models.BooleanField(
        _('accept subscriptions'),
        default=True,
        help_text=_(
            'Set it to false to prevent new student subscriptions.'
        ),
    )
    is_public = models.BooleanField(
        _('is it public?'),
        default=False,
        help_text=_(
            'If true, all students will be able to see the contents of the '
            'course. Most activities will not be available to non-subscribed '
            'students.'
        ),
    )
    comments_policy = models.EnumField(
        CommentPolicyEnum,
        blank=True, null=True,
    )
    subscription_passphrase = models.CharField(
        _('subscription passphrase'),
        default=phrase_lower,
        max_length=140,
        help_text=_(
            'A passphrase/word that students must enter to subscribe in the '
            'course. Leave empty if no passphrase should be necessary.'
        ),
        blank=True,
    )
    objects = ClassroomManager()

    def register_student(self, user):
        """
        Register a new student in the course.
        """

        if user == self.teacher:
            raise ValidationError(_('Teacher cannot enroll as student.'))
        elif self.staff.filter(id=user.id):
            raise ValidationError(_('Staff member cannot enroll as student.'))
        self.students.add(user)

    def register_staff(self, user):
        """
        Register a new user as staff.
        """

        if user == self.teacher:
            raise ValidationError(_('Teacher cannot enroll as staff.'))
        self.students.add(user)


@rest_api
class Organization(DescriptiveModel):
    """
    A basic organizational entity in a an school or university.

    Can be an department, a campus, a specific branch or represent the whole
    institution itself.
    """


@rest_api
class Discipline(DescriptiveModel):
    """
    An academic discipline.
    """

    organization = models.ForeignKey(
        'Organization',
        blank=True,
        on_delete=models.CASCADE,
    )
    school_id = models.CharField(
        max_length=50,
        blank=True
    )
    since = models.DateField(blank=True, null=True)

    # These were modeled as in https://matriculaweb.unb.br/, which is not
    # particularly good. In the future we may want more structured data types.
    syllabus = models.TextField(blank=True)
    program = models.TextField(blank=True)
    bibliography = models.TextField(blank=True)


class Topic(models.Model):
    """
    A topic in a classroom
    """

    name = models.NameField()
    index = models.PositiveSmallIntegerField()
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('name', 'classroom')]

    def __str__(self):
        return self.name
