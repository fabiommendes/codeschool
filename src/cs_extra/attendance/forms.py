from django.forms import ModelForm

from . import models


class PassphraseForm(ModelForm):
    """
    A form with a single 'passphrase' value.
    """

    class Meta:
        fields = ('passphrase',)
        model = models.Event
