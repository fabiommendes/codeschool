from boogie import models
from boogie.fields.enum_type import IntEnum


class PollType(IntEnum):
    MULTIPLE_CHOICE = 0, _('Multiple choice')
    FREE_TEXT = 0, _('Free text')


class AbstractTimelineItem(models.TimeStampedModel):
    # status = models.StatusField() Posted, Draft, Scheduled
    classroom = models.ForeignKey(
        'classrooms.Classroom',
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        'classrooms.Topic',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    hyperlink = models.URLField(blank=True)
    attachment = models.FileField(
        blank=True, null=True,
        upload_to='classrooms/timeline/notice',
    )

    class Meta:
        abstract = True


class Notice(AbstractTimelineItem):
    pass


class AbstractTask(models.TimeFramedModel, AbstractTimelineItem):
    class Meta:
        abstract = True


class Task(AbstractTask):
    instructions = models.TextField()


class Poll(AbstractTask):
    kind = models.EnumField(PollType)


class PollChoice(models.Model):
    title = models.TitleField()
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(default=0)
