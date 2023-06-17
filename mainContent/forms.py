from django import forms
from .models import RaportsUnlogged


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RaportForm(forms.ModelForm):
    class Meta:
        model = RaportsUnlogged
        widgets = {
            'content': forms.Textarea(attrs={'id': 'report_opinion', 'rows': "16", "cols": "75"}),
        }
        fields = ["content",]
        labels = {"content": "",}

