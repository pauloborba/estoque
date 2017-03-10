from django import forms

class LoginForm(forms.Form):
    username = forms.charField()
    pwd = forms.charField(widget=forms.PasswordInput)
