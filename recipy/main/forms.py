from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
