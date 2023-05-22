import re

from django import forms
from captcha.fields import CaptchaField

from ehms.core.utils import RELATIONS


class FamilyRelationForm(forms.Form):
    """
    Family Relation form to create relation between the patients
    """
    first_patient = forms.RegexField(
        label='First Patient',
        error_messages={
            'required': 'First patient UID is required.',
            'invalid': 'First patient UID is invalid'
        },
        strip=True,
        regex=re.compile(r'^\d{12}$'),
    )

    first_to_second_relation = forms.ChoiceField(
        label='First patient relation to second patient',
        widget=forms.Select,
        error_messages={
            'required': 'Choose relation between first to second patient.',
            'invalid': 'Your choice is invalid.'
        },
        choices=RELATIONS,
    )

    second_patient = forms.RegexField(
        label='Second Patient',
        error_messages={
            'required': 'Second patient UID is required.',
            'invalid': 'Second patient UID is invalid'
        },
        strip=True,
        regex=re.compile(r'^\d{12}$'),
    )

    second_to_first_relation = forms.ChoiceField(
        label='Second patient relation to first patient',
        widget=forms.Select,
        error_messages={
            'required': 'Choose relation between second to first patient.',
            'invalid': 'Your choice is invalid.'
        },
        choices=RELATIONS,
    )

    first_patient.widget.attrs.update({
        'class': 'form-control', 'placeholder': 'Enter first patient UID',
        'data-validation': 'required'
    })
    second_patient.widget.attrs.update({
        'class': 'form-control', 'placeholder': 'Enter second patient UID',
        'data-validation': 'required'
    })
    first_to_second_relation.widget.attrs.update({
        'class': 'form-select', 'data-validation': 'required'
    })
    second_to_first_relation.widget.attrs.update({
        'class': 'form-select', 'data-validation': 'required'
    })

