'''
from django import forms

class AccountForm(forms.Form):
    # these fields must map to the HTML form's input elements
    firstname = forms.CharField(max_length=240)
    surname = forms.CharField(max_length=240)
    email = forms.EmailField()
    address = forms.CharField(max_length=240)
    birthdate = forms.DateField()
    image = forms.ImageField()
    bio = forms.CharField(widget=forms.Textarea, max_length=240)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
'''

from django.contrib.auth.models import User

from django import forms
from .models import Profile


class PostForm(forms.Form):
    text = forms.CharField()
    image = forms.FileField()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }


# class UserUpdateForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput())
#     confirm_password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = [['username', 'last_name', 'first_name', 'email', 'password']]

#     def clean(self):
#         cleaned_data = super(UserUpdateForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             self.add_error("confirm_password", "Password does not match")
#         return cleaned_data



# class ProfileUpdateForm(forms.Form):
#     class Meta:
#         model = Profile
#         fields = ['image']
