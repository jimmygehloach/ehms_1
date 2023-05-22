import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import VitalSignRecord, IntakeOutputChart, NurseNotes


class NewVitalSignRecordForm(forms.ModelForm):

    class Meta:
        model = VitalSignRecord
        fields = [
            'bed_number', 'pulse', 'temperature',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'height', 'weight',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bed_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['pulse'].widget.attrs.update({'class': 'form-select'})
        self.fields['temperature'].widget.attrs.update({'class': 'form-select'})
        self.fields['blood_pressure_systolic'].widget.attrs.update({'class': 'form-control'})
        self.fields['blood_pressure_diastolic'].widget.attrs.update({'class': 'form-control'})
        self.fields['height'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})


class NewIntakeOutputChartForm(forms.ModelForm):

    class Meta:
        model = IntakeOutputChart
        fields = [
            'bed_number', 'intake_timings', 'output_timings', 'intake_oral',
            'intake_iv_fluids', 'output_urine', 'output_vomit', 'output_suction',
            'output_drain',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bed_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['intake_timings'].widget.attrs.update({'class': 'form-control'})
        self.fields['output_timings'].widget.attrs.update({'class': 'form-control'})
        self.fields['intake_oral'].widget.attrs.update({'class': 'form-control'})
        self.fields['intake_iv_fluids'].widget.attrs.update({'class': 'form-control'})
        self.fields['output_urine'].widget.attrs.update({'class': 'form-control'})
        self.fields['output_vomit'].widget.attrs.update({'class': 'form-control'})
        self.fields['output_suction'].widget.attrs.update({'class': 'form-control'})
        self.fields['output_drain'].widget.attrs.update({'class': 'form-control'})


class NewNurseNotesForm(forms.ModelForm):

    class Meta:
        model = NurseNotes
        fields = [
            'bed_number', 'timings', 'observation',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bed_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['timings'].widget.attrs.update({'class': 'form-control'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control'})


class NurseTokenForm(forms.Form):
    """
    Form to generate token for nurses
    """
    token_timestamp = forms.RegexField(
        label='Token Valid upto (Select the date and time)',
        error_messages={
            'required': 'Select the token date and time',
            'invalid': 'Token data and time is invalid'
        },
        strip=True,
        regex=re.compile(r'^(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2})$'),
    )

    nurse = forms.ModelChoiceField(
        label='Choose nurse whose token you want to generate.',
        widget=forms.Select,
        queryset=None,
        error_messages={
            'required': 'Choose the nurse from dropdown.',
            'invalid': 'Nurse is invalid.'
        },
        empty_label="---------------------"
    )

    token_timestamp.widget.attrs.update({'class': 'form-control', 'id': 'token-valid-upto'})
    nurse.widget.attrs.update({'class': 'form-select', 'id': 'token-nurse'})

