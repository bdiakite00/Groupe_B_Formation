from django import forms
from .models import GoogleSheet
from django.utils.translation import gettext_lazy as _
class GoogleSheetForm(forms.ModelForm):
    class Meta:
        model = GoogleSheet
        fields = ['lien_google_sheet']
        widgets = {
            'lien_google_sheet': forms.URLInput(attrs={'class': 'form-control', 'placeholder': _('Entrez le lien Google Sheet ici')}),
        }
