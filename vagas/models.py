from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User

class Empresa(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Vaga(models.Model):
    SALARIO_VAGAS_CHOICES = [
        ('0-1000', 'Até 1.000'),
        ('1000-2000', 'De 1.000 a 2.000'),
        ('2000-3000', 'De 2.000 a 3.000'),
        ('3000+', 'Acima de 3.000'),
    ]

    EDUCACAO_CHOICES = [
        ('Fundamental', 'Ensino Fundamental'),
        ('Medio', 'Ensino Médio'),
        ('Tecnologo', 'Tecnólogo'),
        ('Superior', 'Ensino Superior'),
        ('Pós', 'Pós / MBA / Mestrado'),
        ('Doutorado', 'Doutorado'),
    ]

    titulo = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=20, choices=SALARIO_VAGAS_CHOICES)
    requerimentos = models.TextField()
    ensino_minimo = models.CharField(max_length=20, choices=EDUCACAO_CHOICES)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_vagas')


class Candidato(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')
    expectativa_salarial = models.DecimalField(max_digits=10, decimal_places=2)
    experiencia = models.TextField()
    ensino_ultimo = models.CharField(max_length=20, choices=Vaga.EDUCACAO_CHOICES)

    def __str__(self):
        return f'{self.ensino_ultimo} - {self.expectativa_salarial}'

    def calcular_score(self):
        score = 0

        # Adiciona 1 ponto se o candidato está dentro da faixa salarial da vaga
        if self._is_salario_dentro_faixa():
            score += 1

        # Adiciona 1 ponto se a escolaridade do candidato é compatível ou maior que o mínimo exigido pela vaga
        if self._is_educacao_compatível():
            score += 1

        return score

    def _is_salario_dentro_faixa(self):
        """Verifica se a expectativa salarial do candidato está dentro da faixa salarial da vaga"""
        faixa = self.vaga.faixa_salarial

        if faixa == '0-1000' and self.expectativa_salarial <= Decimal('1000'):
            return True
        if faixa == '1000-2000' and Decimal('1000') < self.expectativa_salarial <= Decimal('2000'):
            return True
        if faixa == '2000-3000' and Decimal('2000') < self.expectativa_salarial <= Decimal('3000'):
            return True
        if faixa == '3000+' and self.expectativa_salarial > Decimal('3000'):
            return True

        return False

    def _is_educacao_compatível(self):
        """Verifica se o nível de ensino do candidato é compatível com o mínimo exigido pela vaga"""
        niveis_educacionais = [
            'Fundamental', 'Medio', 'Tecnologo', 'Superior', 'Pós', 'Doutorado'
        ]
        ensino_minimo = self.vaga.ensino_minimo
        indice_minimo = niveis_educacionais.index(ensino_minimo)
        indice_candidato = niveis_educacionais.index(self.ensino_ultimo)

        return indice_candidato >= indice_minimo
