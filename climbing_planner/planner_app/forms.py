from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="")
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")

    username.widget.attrs.update({
        'placeholder': 'username',
        'class':'validate',
        'data-length': '64',
    })
    password.widget.attrs.update({
        'placeholder': 'password',
        'class': 'validate',
    })

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64, label="")
    email = forms.EmailField()
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="")
    is_instructor = forms.BooleanField(required=False)

    username.widget.attrs.update({
        'placeholder': 'username',
        'class':'validate',
        'data-length': '64',
    })
    email.widget.attrs.update({
        'placeholder': 'email',
        'class':'validate',
        'data-length': '64',
    })
    password.widget.attrs.update({
        'placeholder': 'password',
        'class': 'validate',
    })

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    email.widget.attrs.update({
        'placeholder': 'email',
        'class':'validate',
        'data-length': '64',
    })
