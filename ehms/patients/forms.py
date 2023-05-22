from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models
from ..addresses.models import Postcode


class NewShortRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['date_of_birth'].widget.attrs.update(
            {'class': 'form-control', 'id': 'patient-registration-datepicker', 'autocomplete': 'off'})

        self.fields['gender'].widget.attrs.update({'class': 'form-select', 'autocomplete': 'off'})


class PatientDeathRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['died_on'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'tabindex': '14',
            'data-validation': 'required',
        })

        self.fields['reason'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'tabindex': '14',
            'data-validation': 'required',
        })

        self.fields['place'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'tabindex': '14',
            'data-validation': 'required',
        })

        self.fields['notes'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'tabindex': '14',
            'data-validation': 'max:20000',
        })

    class Meta:
        model = models.PatientDeathRecord
        fields = [
            'died_on',
            'reason',
            'place',
            'notes',
        ]


class PatientImageUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'tabindex': '14',
            'data-validation': 'required|file:jpg,jpeg:2:MB',
            'help-text': _('Try to upload a square photo for better result. Recommended(500 X 500)')
        })

    class Meta:
        model = models.PatientImage
        fields = ['image']


class NewPatientRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---------------------------------------------------------------------------------- Patient General Information

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'required|max:100|min:1|alpha',
            'tabindex': '1',
            'autofocus': 'autofocus'
        })

        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'max:100|min:1|alpha',
            'tabindex': '2'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'required|max:100|min:1|alpha',
            'tabindex': '3'
        })

        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'required|checkDate:yyyy-mm-dd',
            'tabindex': '4'
        })

        self.fields['gender'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required|within:Male,Female,Transgender',
            'tabindex': '5'
        })

        self.fields['religion'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'tabindex': '6',
            'data-validation': 'within:Islam,Christianity,Baha i Faith,African Traditional Faith,Hinduism,Buddhism,'
                               'Folk religions,Sikhism,Judaism,Others,No Religion|required'
        })

        self.fields['marital_status'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'tabindex': '7',
            'data-validation': 'required|within:Married,Unmarried,Divorced,Widow,Widower'
        })

        self.fields['pregnancy'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'tabindex': '8',
            'data-validation': 'required|within:Pregnant,Not Pregnant,Not Applicable'
        })

        self.fields['children'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'required|digit|max:100',
            'tabindex': '9'
        })

        self.fields['blood_group'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'tabindex': '10',
            'data-validation': 'within:A Positive,O Positive,B Positive,AB Positive,A Negative,'
                               'O Negative,B Negative,AB Negative'
        })

        self.fields['height'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'number|max:350:number|min:5:number',
            'tabindex': '11'
        })

        self.fields['weight'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'number|max:1000:number|min:1:number',
            'tabindex': '12'
        })

        self.fields['disability'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
        })

        # ---------------------------------------------------------------------------------- Patient Medical Information

        self.fields['patient_medical_illness'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
        })

        self.fields['patient_kin_medical_illness'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
        })

        self.fields['patient_allergies'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
        })

        self.fields['patient_addictions'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
        })

        # ----------------------------------------------------------------------------- Patient Immunization Information

        self.fields['bcg'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['pentavalent'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['pneumo'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['polio'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['rotarix'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['measles_rubella_1'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['measles_rubella_2'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['dpt'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['yellow_fever'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['vitamin_a'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        self.fields['tetanus'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off'
        })

        # ------------------------------------------------------------------------------------ Patient Misc. Information

        self.fields['remarks'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'Remarks related to patient, if any...',
        })

        self.fields['other_information'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'You can write down extra information related to patient here...',
        })

        self.fields['temporary_family_info'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'You can write down more about patient\'s family information here...'
        })

    class Meta:
        model = models.Patient
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'religion',
            'marital_status',
            'pregnancy',
            'children',
            'blood_group',
            'height',
            'weight',
            'disability',
            ##################
            'patient_medical_illness',
            'patient_kin_medical_illness',
            'patient_allergies',
            'patient_addictions',
            ##################
            'bcg',
            'pentavalent',
            'pneumo',
            'polio',
            'rotarix',
            'measles_rubella_1',
            'measles_rubella_2',
            'dpt',
            'yellow_fever',
            'vitamin_a',
            'tetanus',
            ##################
            'remarks',
            'other_information',
            'temporary_family_info',
        ]


class NewPatientAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ------------------------------------------------------------------------------------- New Patient Address Form

        self.fields['address_line_1'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'required|address|max:250|min:1',
            'tabindex': '15'
        })

        self.fields['address_line_2'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'address|max:250|min:1',
            'tabindex': '16'
        })

        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'phone:uk',
            'tabindex': '17'
        })

        self.fields['alternate_phone'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'data-validation': 'phone:uk',
            'tabindex': '18'
        })

        self.fields['type'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'within:Temporary,Permanent',
            'tabindex': '19'
        })

        self.fields['current_address'].widget.attrs.update({
            'class': 'form-check-input',
            'autocomplete': 'off',
            'tabindex': '20'
        })

        self.fields['country'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required',
            'tabindex': '20'
        })

        self.fields['region'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required',
            'tabindex': '21'
        })

        self.fields['district'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required',
            'tabindex': '22'
        })

        self.fields['town'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required',
            'tabindex': '23'
        })

        self.fields['postcode'].widget.attrs.update({
            'class': 'form-select',
            'autocomplete': 'off',
            'data-validation': 'required',
            'tabindex': '24'
        })

    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     try:
    #         Postcode.objects.get(
    #             status='active',
    #             country=cleaned_data.get('country'),
    #             region=cleaned_data.get('region'),
    #             district=cleaned_data.get('district'),
    #             town=cleaned_data.get('town')
    #         )
    #     except Postcode.DoesNotExist:
    #         raise ValidationError(
    #             _('Address is invalid. Check country, region, district, town, postcode fields.'),
    #             code='invalid',
    #             params={},
    #         )

    class Meta:
        model = models.PatientAddress
        fields = [
            'address_line_1',
            'address_line_2',
            'phone',
            'alternate_phone',
            'type',
            'current_address',
            'country',
            'region',
            'district',
            'town',
            'postcode'
        ]


class UpdatePatientGeneralInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['uid'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['religion'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['age_group'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off', 'disabled': 'disabled'
        })

    class Meta:
        model = models.Patient
        fields = ['uid', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'religion', 'age_group']


class UpdatePatientPersonalInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['marital_status'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off', 'disabled': 'disabled'
        })
        self.fields['children'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off', 'disabled': 'disabled'
        })

    class Meta:
        model = models.Patient
        fields = ['marital_status', 'children']


class UpdatePatientMedicalInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['blood_group'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'within:A Positive,O Positive,B Positive,AB Positive,A Negative,'
                               'O Negative,B Negative,AB Negative'
        })
        self.fields['patient_medical_illness'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off'
        })
        self.fields['patient_kin_medical_illness'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off'
        })
        self.fields['patient_allergies'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off'
        })
        self.fields['patient_addictions'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off'
        })

    class Meta:
        model = models.Patient
        fields = ['blood_group', 'patient_medical_illness', 'patient_medical_illness',
                  'patient_kin_medical_illness', 'patient_allergies', 'patient_addictions']


class UpdatePatientPhysicalInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['height'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off',
            'data-validation': 'number|max:350|min:5',
        })
        self.fields['weight'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off',
            'data-validation': 'number|max:1000|min:1',
        })
        self.fields['disability'].widget.attrs.update({
            'class': 'form-check-input', 'autocomplete': 'off'
        })

    class Meta:
        model = models.Patient
        fields = ['height', 'weight', 'disability', ]


class UpdatePatientImportantInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['health_status'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required'
        })

    class Meta:
        model = models.Patient
        fields = ['health_status']


class UpdatePatientMiscInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['other_information'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'You can write down extra information related to patient here...'
        })

        self.fields['temporary_family_info'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'You can write down more about patient\'s family information here...'
        })

        self.fields['remarks'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off',
            'rows': 3,
            'placeholder': 'Remarks related to patient, if any...'
        })

    class Meta:
        model = models.Patient
        fields = ['other_information', 'remarks', 'temporary_family_info']


class UpdatePatientImmunizationInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bcg'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['pentavalent'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['pneumo'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['polio'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['rotarix'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['measles_rubella_1'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['measles_rubella_2'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['dpt'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['yellow_fever'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['vitamin_a'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})
        self.fields['tetanus'].widget.attrs.update({'class': 'form-check-input', 'autocomplete': 'off'})

    class Meta:
        model = models.Patient
        fields = [
            'bcg', 'pentavalent', 'pneumo', 'polio', 'rotarix', 'measles_rubella_1', 'measles_rubella_2', 'dpt',
            'yellow_fever', 'vitamin_a', 'tetanus',
        ]


class UpdatePatientFemaleInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pregnancy'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required|within:Pregnant,Not Pregnant,Not Applicable'
        })
        self.fields['tt_one_pregnant'].widget.attrs.update({
            'class': 'form-check-input', 'autocomplete': 'off'
        })
        self.fields['tt_two_pregnant'].widget.attrs.update({
            'class': 'form-check-input', 'autocomplete': 'off'
        })
        self.fields['tt_booster'].widget.attrs.update({
            'class': 'form-check-input', 'autocomplete': 'off'
        })

    class Meta:
        model = models.Patient
        fields = ['pregnancy', 'tt_one_pregnant', 'tt_two_pregnant', 'tt_booster']


class PatientDocumentUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off',
            'data-validation': 'required|alphaNum:space:comma:hyphen:dot:brackets'
        })
        self.fields['type'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off',
            'data-validation': 'required|alphaNum:space:comma:hyphen:dot:brackets'
        })
        self.fields['document'].widget.attrs.update({
            'class': 'form-control', 'autocomplete': 'off',
            'data-validation': 'required|file:pdf:5:MB'
        })

    class Meta:
        model = models.PatientDocument
        fields = [
            'name', 'type', 'document',
        ]


class UpdatePatientHospitalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['hospital'].widget.attrs.update({
            'class': 'form-select', 'autocomplete': 'off',
            'data-validation': 'required',
        })

    class Meta:
        model = models.Patient
        fields = [
            'hospital'
        ]
