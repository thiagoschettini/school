# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

# Create your models here.

SERIES = (
    ('1 Serie', '1ª Série'),
    ('2 Serie', '2ª Série'),
    ('3 Serie', '3ª Série'),
    ('4 Serie', '4ª Série'),    
)

ROLES = (
    ('professor','Professor'),
    ('aluno','Aluno'),
    ('secretaria','Secretaria'),    
)

class userProfile(models.Model):
	user = models.ForeignKey(User, unique=True, verbose_name=u'Usuário', help_text=u'Este campo associa o Usuário a uma conta no sistema')
	role = models.CharField(choices=ROLES,max_length=50)

	def __unicode__(self):
		return self.user.username

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
	user = models.ForeignKey(userProfile, unique=True, verbose_name=u'Usuário', help_text=u'Este campo associa o Usuário a uma conta no sistema')
	#turma = models.ManyToManyField(Turma)
	#materia = models.ManyToManyField(Grade)

	def __unicode__(self):
		return self.nome

class Grade(models.Model):
	materia = models.CharField(blank=False, null=False, verbose_name='Matéria',max_length=50)
	professor = models.ForeignKey(Professor)

	def __unicode__(self):
		return '%s - %s' % (self.materia, self.professor.user)

	def totalNotas(self, aluno):
		aluno = get_object_or_404(Aluno, pk=aluno)
		notas = DiarioNotas.objects.filter(materia=self, aluno=aluno)
		total = 0
		for nota in notas:
			total += float(nota.nota)
		return total

	def totalFaltas(self, aluno):
		aluno = get_object_or_404(Aluno, pk=aluno)
		faltas = DiarioFaltas.objects.filter(materia=self, aluno=aluno)
		total = 0
		for falta in faltas:
			total += 1
		return total

class Turma(models.Model):
	serie = models.ForeignKey(Serie, blank=False)
	nomeSala = models.ForeignKey(NomeSala, blank=False)
	#professor = models.ManyToManyField(Professor)
	materia = models.ManyToManyField(Grade)

	def __unicode__(self):
		return '%s %s' % (self.serie, self.nomeSala)

class Aluno(models.Model):
	matricula = models.CharField(blank=False, null=False, verbose_name='Número de Matrícula',max_length=50)
	nomeAluno = models.CharField(blank=False, null=False, verbose_name="Nome do Aluno",max_length=50)
	dataNascimento = models.DateField(blank=False, verbose_name="Data de nascimento")

	user = models.ForeignKey(userProfile, unique=True, null=True, blank=True, verbose_name=u'Usuário', help_text=u'Este campo associa o Usuário a uma conta no sistema')
	turma = models.ForeignKey(Turma, blank=False)

	def __unicode__(self):
		return self.nomeAluno

	def getFaltas(self):
		faltas = DiarioFaltas.objects.filter(aluno=self).order_by('data')
		return faltas

	def getNotas(self):
		notas = DiarioNotas.objects.filter(aluno=self).order_by('materia')
		return notas

	def total(self):
		return self.count

class DiarioNotas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	nota = models.CharField(blank=False, null=False, verbose_name="Nota",max_length=50)
	valor = models.CharField(blank=True, null=False, verbose_name="Pontos distrbuídos",max_length=50)
	referente = models.CharField(blank=False, null=True, verbose_name="Referente a",max_length=255)

	def __unicode__(self):
		return self.aluno.nomeAluno

class DiarioFaltas(models.Model):
	aluno = models.ForeignKey(Aluno, blank=False)
	materia = models.ForeignKey(Grade, blank=False)
	data = models.DateField(blank=False, verbose_name="Data da falta")

	def __unicode__(self):
		return self.aluno.nomeAluno


class Mensagens(models.Model):
	para = models.ForeignKey(User, verbose_name=u'Para', related_name='to')
	destinatario = models.ForeignKey(User, verbose_name=u'De',related_name='from')
	lida = models.BooleanField(blank=True,default='False')
	assunto = models.CharField(blank=False, null=True, verbose_name='Assunto', max_length="150")
	mensagem = models.TextField(blank=False)
	data_envio = models.DateTimeField(blank=True, default='', null=True, verbose_name=u'Data da Mensagem')
	data_lida = models.DateTimeField(blank=True, default='', null=True, verbose_name=u'Data de Leitura')

	def __unicode__(self):
		return u'[%s] - %s (%s)' % (self.data_envio, self.para, self.assunto)