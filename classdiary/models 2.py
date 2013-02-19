# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

SERIES = (
    ('1 Serie', '1ª Série'),
    ('2 Serie', '2ª Série'),
    ('3 Serie', '3ª Série'),
    ('4 Serie', '4ª Série'),    
)

class Grade(models.Model):
	materia = models.CharField(blank=False, null=False, verbose_name='Matéria',max_length=50)

	def __unicode__(self):
		return self.materia

class Serie(models.Model):
	serie = models.CharField(choices=SERIES,max_length=50)

	def __unicode__(self):
		return self.serie

class NomeSala(models.Model):
	nome = models.CharField(blank=False, null=False, verbose_name='Sala', help_text='Nome ou código da sala',max_length=50)

	def __unicode__(self):
		return self.nome

class Professor(models.Model):
	nome = models.CharField(blank=False, null=False, verbose_name='Nome do professor',max_length=50)
	user = models.ForeignKey(User, unique=True, verbose_name=u'Usuário', help_text=u'Este campo associa o Usuário a uma conta no sistema')
	#turma = models.ManyToManyField(Turma)
	materia = models.ManyToManyField(Grade)

	def __unicode__(self):
		return self.nome

class Turma(models.Model):
	serie = models.ForeignKey(Serie, blank=False)
	nomeSala = models.ForeignKey(NomeSala, blank=False)
	professor = models.ManyToManyField(Professor)

	def __unicode__(self):
		return '%s %s' % (self.serie, self.nomeSala)

class Aluno(models.Model):
	matricula = models.CharField(blank=False, null=False, verbose_name='Número de Matrícula',max_length=50)
	nomeAluno = models.CharField(blank=False, null=False, verbose_name="Nome do Aluno",max_length=50)
	dataNascimento = models.DateField(blank=False, verbose_name="Data de nascimento")

	turma = models.ForeignKey(Turma, blank=False)

	def __unicode__(self):
		return self.nomeAluno

class DiarioNotas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	nota = models.CharField(blank=False, null=False, verbose_name="Nota",max_length=50)

	def __unicode__(self):
		return self.aluno.nomeAluno

class DiarioFaltas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	data = models.DateTimeField(blank=False, verbose_name="Data da falta")

	def __unicode__(self):
		return self.aluno.nomeAluno