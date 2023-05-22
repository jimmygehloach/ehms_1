from django import forms

from . import models
from ehms.accounts.models import EHMSUser


class UserRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'data-validation': 'required'
        })
        self.fields['document'].widget.attrs.update({
            # TODO file upload validation
            'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'
        })

    class Meta:
        model = models.Hospital
        fields = ['description', 'document']


