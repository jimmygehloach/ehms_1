from django import forms

from ehms.mortuaries.models import MortuaryPatient


class NewMortuaryPatientForm(forms.ModelForm):
    class Meta:
        model = MortuaryPatient
        fields = [
            'mortuary',
            'date_received',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mortuary'].widget.attrs.update({
            'class': 'form-select', 'data-validation': 'required'
        })
        self.fields['date_received'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'required'
        })


class ReleaseMortuaryPatientForm(forms.ModelForm):
    class Meta:
        model = MortuaryPatient
        fields = [
            'date_released',
            'reason_behind_release',
            'next_of_kin',
            'next_of_kin_relationship',
            'non_relative_person',
            'person_address',
            'person_phone',
            'witness',
            'witness_address',
            'witness_phone',
            'person_uid',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_released'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'required'
        })
        self.fields['reason_behind_release'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'required'
        })
        self.fields['next_of_kin'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'alphaNum:space:brackets|max:100'
        })
        self.fields['next_of_kin_relationship'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['non_relative_person'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'alphaNum:space:brackets|max:100'
        })
        self.fields['person_address'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'address'
        })
        self.fields['person_phone'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'phone'
        })
        self.fields['witness'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'alphaNum:space:brackets|max:100'
        })
        self.fields['witness_address'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'address'
        })
        self.fields['witness_phone'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'phone'
        })
        self.fields['person_uid'].widget.attrs.update({
            'class': 'form-control', 'data-validation': 'uuid'
        })
