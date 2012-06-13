from django.db import models

# Create your models here.

SERIES = (
    ('1', '1ª Série'),
    ('2', '2ª Série'),
    ('3', '3ª Série'),
    ('4', '4ª Série'),    
)

class Turma(models.Model):
	serie = model.CharField(choices=SERIES)
	nomeSala = models.CharField(blank=false, null=false, verbose_name='Sala', help_text='Nome ou código da sala')

class Alunos(models.Model):
	matricula = models.CharField(blank=false, null=false, verbose_name='Número de Matrícula')
	nomeAluno = models.CharField(blank=false, null=false, verbose_name="Nome do Aluno")
	dataNascimento = models.DateTimeField(blank=false, verbose_name="Data de nascimento")
	
	turma = models.ForeignKey(Turma, blank=false)
