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
        # send email using the self.leaned_data dictionary
        pass
'''

from django.contrib.auth.models import User

from django import forms
from .models import Profile


class PostForm(forms.Form):
    text = forms.CharField()
    image = forms.FileField()

class UserUpdateForm(forms.Form):
    class Meta:
        model = User
        fields = [['username', 'last_name', 'first_name', 'email']]

class ProfileUpdateForm(forms.Form):
    
    class Meta:
        model = Profile
        fields = ['image']