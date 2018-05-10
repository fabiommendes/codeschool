from django.utils.translation import ugettext_lazy as _

from boogie import models


class DescriptiveModel(models.TimeStampedModel):
    """
    Abstract Base Class for models with slug/name/description fields.

    Slug is used as a primary key.
    """

    name = models.NameField()
    description = models.ShortDescriptionField(blank=True)
    slug = models.AutoSlugField(
        primary_key=True,
        help_text=_('Unique identifier used to construct urls'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return '%s (%s)' % (self.name, self.slug)