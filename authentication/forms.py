from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].help_text = None
            self.fields[field].widget.attrs.update({
                'placeholder': field.capitalize(),
            })

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': field.capitalize(),
            })
