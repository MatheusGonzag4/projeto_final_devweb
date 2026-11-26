from django import forms
from .models import Servico


class FormServico(forms.ModelForm):
    ativo = forms.BooleanField(label="Ativo", required=False, initial=True)

    class Meta:
        model = Servico
        fields = ("nome", "descricao", "preco", "categoria", "imagem", "ativo")
        labels = {
            "descricao": "Descrição",
            "preco": "Preço",
            "imagem": "Imagem",
        }
        widgets = {"descricao": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].empty_label = "Selecione uma categoria"

