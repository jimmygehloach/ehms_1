from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class HospitalGeneralInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['uid'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})

    class Meta:
        model = models.Hospital
        fields = ['uid', 'name', 'image']


class HospitalLocationInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['longitude'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['latitude'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})

    class Meta:
        model = models.Hospital
        fields = ['longitude', 'latitude']


class HospitalContactInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['alternate_phone'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})

    class Meta:
        model = models.Hospital
        fields = ['phone', 'alternate_phone', 'email']


class HospitalAddressInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address_line_1'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['address_line_2'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['town'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['district'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['region'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['country'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['postcode'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})

    class Meta:
        model = models.Hospital
        fields = ['address_line_1', 'address_line_2', 'town', 'district', 'region', 'country', 'postcode']


class HospitalRepresentativeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['gender'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['designation'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['alternate_phone'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
        self.fields['remarks'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true', 'rows': 5})

    class Meta:
        model = models.HospitalRepresentative
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'designation', 'phone', 'alternate_phone',
                  'email', 'image', 'remarks']


class HospitalUserForm(forms.ModelForm):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #     self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #     self.fields['phone'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #     self.fields['email'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #     self.fields['designation'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #     self.fields['user_unique_id'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'readonly': 'true'})
    #
    # class Meta:
    #     model = User
    #     fields = ['first_name', 'last_name', 'phone', 'email', 'designation', 'user_unique_id']
