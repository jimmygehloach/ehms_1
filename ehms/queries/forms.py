from django import forms

from .import models


class NewHospitalQueryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['attachment'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    class Meta:
        model = models.HospitalQuery
        fields = [
            'subject', 'body', 'attachment',
        ]


class NewPractitionerQueryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['attachment'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    class Meta:
        model = models.PractitionerQuery
        fields = [
            'subject', 'body', 'attachment',
        ]