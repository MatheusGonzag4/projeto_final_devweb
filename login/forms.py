from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):

    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nome de usuário',
        }

    # o e-mail é usado na recuperação de senha, então não pode se repetir
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com esse e-mail.")

        return email


class PerfilForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Digite seu nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Digite seu sobrenome'}),
        }
