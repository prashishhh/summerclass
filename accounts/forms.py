from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control',
            'autocomplete': 'new-password',
            'spellcheck': 'false',
            'autocapitalize': 'off',
            'autocorrect': 'off',
            'inputmode': 'text',
        }),
        strip=False,  # ← IMPORTANT: do not strip passwords
    )
confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control',
        'autocomplete': 'new-password',
        'spellcheck': 'false',
        'autocapitalize': 'off',
        'autocorrect': 'off',
        'inputmode': 'text',
    }),
    strip=False,  # ← IMPORTANT
)

class Meta:
    model = Account
    fields = [
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'password',
    ]
# Assigns class form-control to all classes
def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
    self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
    self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
    self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
    for field in self.fields:
        self.fields[field].widget.attrs['class'] = 'form-control'

def clean(self):
    # We use super class to modify default actions
    cleaned_data = super(RegistrationForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password and confirm_password and password != confirm_password:
        raise forms.ValidationError(
            "Password does not match!"
        )
    return cleaned_data
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "gender", "profile_picture"]
        # widgets = {
        #     "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
        #     "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
        #     "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
        #     "gender": forms.Select(attrs={"class": "form-control"}),
        # }

        # Override default widget for profile_picture:
        # By default, Django uses ClearableFileInput, which shows:
        #   "Currently: <file path>" and a "Clear" checkbox.
        # We replace it with FileInput to hide that text/checkbox
        # because we already display a custom image preview in the template.
        widgets = {
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Loop through all fields and add Bootstrap’s form-control class for styling
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
