from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="")
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")
    username.widget.attrs.update({'placeholder': 'username'})
    password.widget.attrs.update({'placeholder': 'password'})
