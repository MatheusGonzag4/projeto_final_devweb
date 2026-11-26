from django import forms
from .models import Contato


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ("nome", "telefone", "email", "mensagem")
        labels = {"mensagem": "Mensagem"}
        widgets = {"mensagem": forms.Textarea(attrs={"rows": 7})}
