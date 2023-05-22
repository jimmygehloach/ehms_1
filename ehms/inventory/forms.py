from django import forms

from .models import ReceivedDetail, IssuedDetail


class NewReceivedDetailForm(forms.ModelForm):
    class Meta:
        model = ReceivedDetail
        fields = [
            'supplier',
            'gross_amount',
            'remarks',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewIssuedDetailForm(forms.ModelForm):
    class Meta:
        model = IssuedDetail
        fields = [
            'department',
            'gross_amount',
            'remarks',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
