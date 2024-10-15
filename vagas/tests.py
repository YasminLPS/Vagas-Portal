from django.test import TestCase
from .models import Vaga, Empresa

class VagaModelTest(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome='Empresa Exemplo',
            email='empresa@exemplo.com'
        )
        
        self.vaga = Vaga.objects.create(
            titulo='Developer',
            faixa_salarial='1000-2000',
            requerimentos='Python, Django',
            ensino_minimo='Superior',
            empresa=self.empresa
        )

    def test_vaga_criacao(self):
        self.assertEqual(self.vaga.titulo, 'Developer')
        self.assertEqual(self.vaga.faixa_salarial, '1000-2000')
        self.assertEqual(self.vaga.ensino_minimo, 'Superior')
        self.assertEqual(self.vaga.empresa.email, 'empresa@exemplo.com') 
