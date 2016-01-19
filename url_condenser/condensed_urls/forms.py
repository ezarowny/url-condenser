from django import forms


class SubmitUrlForm(forms.Form):
    url = forms.URLField(label='URL to condense:')
