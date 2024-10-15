from django import forms
from .models import Vaga, Candidato, Empresa
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome','email'] 


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo', 'faixa_salarial', 'requerimentos', 'ensino_minimo']

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['expectativa_salarial', 'experiencia', 'ensino_ultimo']
