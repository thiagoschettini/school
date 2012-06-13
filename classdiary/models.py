# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

SERIES = (
    ('1', '1ª Série'),
    ('2', '2ª Série'),
    ('3', '3ª Série'),
    ('4', '4ª Série'),    
)

class Grade(models.Model):
	materia = models.CharField(blank=False, null=False, verbose_name='Matéria',max_length=50)

	def __unicode__(self):
		return self.materia

class Turma(models.Model):
	serie = models.CharField(choices=SERIES,max_length=50)
	nomeSala = models.CharField(blank=False, null=False, verbose_name='Sala', help_text='Nome ou código da sala',max_length=50)

	grade = models.ManyToManyField(Grade)

	def __unicode__(self):
		return '%s %s' % (self.serie, self.nomeSala)

class Aluno(models.Model):
	matricula = models.CharField(blank=False, null=False, verbose_name='Número de Matrícula',max_length=50)
	nomeAluno = models.CharField(blank=False, null=False, verbose_name="Nome do Aluno",max_length=50)
	dataNascimento = models.DateTimeField(blank=False, verbose_name="Data de nascimento")

	turma = models.ForeignKey(Turma, blank=False)

	def __unicode__(self):
		return self.nomeAluno

class Professor(models.Model):
	nome = models.CharField(blank=False, null=False, verbose_name='Nome do professor',max_length=50)

	turma = models.ManyToManyField(Turma)
	materia = models.ManyToManyField(Grade)

	def __unicode__(self):
		return self.nome

class DiarioNotas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	nota = models.CharField(blank=False, null=False, verbose_name="Nota",max_length=50)

	def __unicode__(self):
		return self.aluno

class DiarioFaltas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	faltas = models.CharField(blank=False, null=False, verbose_name="Nota",max_length=50)

	def __unicode__(self):
		return self.aluno