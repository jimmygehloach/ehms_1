from django import forms
from django.forms import FileInput, Select, Textarea, SelectMultiple


from .import models


class NewMedicalSessionForm(forms.ModelForm):
    class Meta:
        model = models.MedicalSession
        fields = [
            'diagnosis', 'medication', 'procedure', 'hard_file',
            'supporting_documents', 'keywords', 'department', 'ward',
            'emergency_session',
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        widgets = {
            'emergency_session': forms.CheckboxInput(attrs={
                'class': 'ms-emergency_session form-control',
                'placeholder': 'Write down the diagnosis of the patient.',
            }),
            'diagnosis': Textarea(attrs={
                'class': 'ms-diagnosis form-control',
                'placeholder': 'Write down the diagnosis of the patient.',
            }),
            'medication': Textarea(attrs={
                'class': 'ms-medication form-control',
                'placeholder': 'Write down the medication of the patient.',
            }),
            'procedure': Textarea(attrs={
                'class': 'ms-procedure form-control',
                'placeholder': 'Write down the medication of the patient.',
            }),
            'hard_file': FileInput(attrs={'class': 'ms-hard-file form-control'}),
            'supporting_documents': FileInput(attrs={'class': 'ms-supporting-docs form-control'}),
            'keywords': SelectMultiple(attrs={'class': 'form-select ms-keywords form-control'}),
            'department': Select(attrs={'class': 'ms-department form-control'}),
            'ward': Select(attrs={'class': 'ms-ward form-control'}),
        }


class NewReceptionMedicalSessionForm(forms.ModelForm):
    class Meta:
        model = models.MedicalSession
        fields = [
           'department', 'ward', 'emergency_session', 'practitioner'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['department'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required', 'tab-index': 1,
        })

        self.fields['ward'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required', 'tab-index': 2,
        })

        self.fields['practitioner'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required', 'tab-index': 3,
        })

        self.fields['emergency_session'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'tab-index': 4
        })
