# -*- coding: utf-8 -*-
from collections import defaultdict
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, UserManager
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext
import datetime

from models import *
from school import settings
from school import forms
from school.forms import *

"""def msgs_count(request):
	m = Mensagens.objects.filter(para=request)
	m = m.filter(lida=False)
	return m.count()
"""
@login_required
def home(request):
	if request.user.get_profile().role == 'professor':
		return HttpResponseRedirect(reverse('home_professor'))
	elif request.user.get_profile().role == 'aluno':
		return HttpResponseRedirect(reverse('home_aluno'))
	else:
		return HttpResponseRedirect(reverse('home_secretaria'))

@login_required
def homeProfessor(request):
	#m = msgs_count(request.user)
	#alunos = Aluno.objects.all()
	#turmas = Turma.objects.all()
	#professores = Professor.objects.all()
	#turma = get_object_or_404(Turma, pk=1)
	#alunoByTurma = Aluno.objects.filter(turma=turma)
	
	#diarioClassDict = {}
	#for aluno in alunoByTurma:
		#diarioClassDict[aluno.nomeAluno] = aluno.nomeAluno
		

	#notas = DiarioNotas.objects.all().order_by('materia__materia')
	#faltas = DiarioFaltas.objects.all()
	#grade_materias = Grade.objects.all()

	#cl =  get_object_or_404(Cliente, pk=request.user.get_profile().pk)
	#prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	#turmas = Turma.objects.filter(professor=prof)
	#prof = request.user.get_profile()
	#diarioClassDict = {}
	#for materia in grade_materias:
	prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	materias = Grade.objects.filter(professor=prof)
	turmas = Turma.objects.filter(materia=materias)
	mensagens = Mensagens.objects.filter(para=request.user.pk, lida=False).order_by('-data_envio')[:5]

	return render_to_response('starter.html', locals(), context_instance=RequestContext(request),)

@login_required
def homeAluno(request):
	return render_to_response('starter.html', locals(), context_instance=RequestContext(request),)	

@login_required
def boletimAluno(request):
	aluno = get_object_or_404(Aluno, user=request.user.get_profile().pk)
	turma = get_object_or_404(Turma, pk=aluno.turma.pk)

	d = defaultdict(list)

	for m in turma.materia.all():
		pair = [aluno, m.totalNotas(aluno=aluno.pk)]
		d[m].append(pair)

	f = defaultdict(list)

	for m in turma.materia.all():
		pair = [aluno, m.totalFaltas(aluno=aluno.pk)]
		f[m].append(pair)
	
	data = dict(d)
	dataFaltas = dict(f)

	return render_to_response('alunoHome.html', locals(), context_instance=RequestContext(request),)

@login_required
def turmaView(request, pk):
	prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	turma = get_object_or_404(Turma, pk=pk)
	grade = Grade.objects.filter(professor=prof, turma=turma)
	alunos = Aluno.objects.filter(turma=turma).order_by('nomeAluno')
	turmas = Turma.objects.filter(materia=grade)
	faltas = DiarioFaltas.objects.all()
	#d = { i: object() for i in alunos }
	
	d = defaultdict(list)

	for a in alunos:
		for m in grade:
			pair = [a, m.totalNotas(aluno=a.pk)]
			d[m].append(pair)

	f = defaultdict(list)

	for a in alunos:
		for m in grade:
			pair = [a, m.totalFaltas(aluno=a.pk)]
			f[m].append(pair)
			#d[a.pk].append(total)
	''' 
	d = defaultdict(list)
	keyLvl1 = 0
	
	for a in alunos:
		d[keyLvl1] = defaultdict(list)
		keyLvl2 = 0
		d[keyLvl1][keyLvl2].append(a)
		for m in grade:
			keyLvl2 += 1
			d[keyLvl1][keyLvl2].append(m)
			notas = DiarioNotas.objects.filter(aluno=a, materia=m)
			total = 0
			for n in notas:
				total += float(n.nota) 
			d[keyLvl1][keyLvl2].append(total)
			
		#d[keyLvl1] = defaultdict(list)
		#d[key] 
		#if key == len(alunos)-1:
		#	d[key+1] = defaultdict(list)
	
		keyLvl1 += 1
	dic = dict(d)
	'''
	data = dict(d)
	dataFaltas = dict(f)
	#d = []
	#key = 1
	#for a in alunos:
	#	for m in grade:
	#		d[key]['nome'] = a.nomeAluno
	#		d[key]['materia'] = m.materia
	#	key += 1 
	return render_to_response('adminView.html', locals(), context_instance=RequestContext(request),)

@login_required
def alunoView(request, pk, filtro):
	prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	grade = Grade.objects.filter(professor=prof)
	aluno = get_object_or_404(Aluno, pk=pk)
	turmas = Turma.objects.filter(materia=grade)

	form = NotasForm()

	if request.method == 'POST':
		
		#dump = request.POST.get('nota')
		# @todo - fazer um foreach para extrair os valores do REQUEST.POST
		materia = get_object_or_404(Grade, pk=request.POST.get('materia'))
		if filtro == 'nota':
			notaNew = DiarioNotas(aluno=aluno, materia=materia, nota=request.POST.get('nota'), valor=request.POST.get('total'), referente=request.POST.get('referente'))
			notaNew.save()
		if filtro == 'falta':
			faltaNew = DiarioFaltas(aluno=aluno, materia=materia, data=request.POST.get('dataFalta'))
			faltaNew.save()

	return render_to_response('alunoView.html', locals(), context_instance=RequestContext(request),)

@login_required
def editFalta(request, pk):
	falta = get_object_or_404(DiarioFaltas, pk=pk)
	aluno = get_object_or_404(Aluno, pk=falta.aluno.pk)
	prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	grade = Grade.objects.filter(professor=prof)
	turmas = Turma.objects.filter(materia=grade)

	if request.method == 'POST':
		#materia = get_object_or_404(Grade, pk=request.POST.get('materia'))
		falta.data = request.POST.get('dataFalta')
		falta.materia = get_object_or_404(Grade, pk=request.POST.get('materia'))
		falta.save()

	return render_to_response('editFalta.html', locals(), context_instance=RequestContext(request),)	

@login_required
def editNota(request, pk):
	nota = get_object_or_404(DiarioNotas, pk=pk)
	aluno = get_object_or_404(Aluno, pk=nota.aluno.pk)
	prof = get_object_or_404(Professor, pk=request.user.get_profile().pk)
	grade = Grade.objects.filter(professor=prof)
	turmas = Turma.objects.filter(materia=grade)

	if request.method == 'POST':
		#materia = get_object_or_404(Grade, pk=request.POST.get('materia'))
		nota.materia = get_object_or_404(Grade, pk=request.POST.get('materia'))
		nota.nota = request.POST.get('nota')
		nota.valor = request.POST.get('total')
		nota.referente = request.POST.get('referente')
		nota.save()

	return render_to_response('editNota.html', locals(), context_instance=RequestContext(request),)	

@login_required
def mensagemLista(request):
	mensagens = Mensagens.objects.filter(para=request.user.pk)
	return render_to_response('mensagensLista.html', locals(), context_instance=RequestContext(request),)

@login_required
def minhasMensagens(request):
	mensagens = Mensagens.objects.filter(destinatario=request.user.pk)
	return render_to_response('mensagensLista.html', locals(), context_instance=RequestContext(request),)	

@login_required
def mensagemDetalhe(request, pk):
	mensagem = get_object_or_404(Mensagens, pk=pk)
	if mensagem.destinatario != request.user:
		mensagem.lida = True
		mensagem.data_lida = datetime.datetime.now()
		mensagem.save()
	return render_to_response('mensagensDetalhe.html', locals(), context_instance=RequestContext(request),)	

@login_required
def mensagemAlunos(request, pk):
	turma = get_object_or_404(Turma, pk=pk)
	alunos = Aluno.objects.filter(turma=turma)
	return render_to_response('selectAlunos.html', locals(), context_instance=RequestContext(request),)

@login_required
def mensagem(request):
	if request.user.get_profile().role == 'professor':
		turmas = Turma.objects.all()
		alunos = Aluno.objects.all()
		if request.method == 'POST':
			sendList = request.POST.getlist('aluno')
			if sendList != []:
				for para in sendList:
					mensagem = Mensagens()
					mensagem.data_envio = datetime.datetime.now()
					mensagem.data_lida = datetime.datetime.now()

					mensagem.assunto = request.POST.get('assunto')
					mensagem.mensagem = request.POST.get('mensagem')
					alunoDest = get_object_or_404(Aluno, pk=para)
					mensagem.para = alunoDest.user.user
					mensagem.destinatario = request.user
					mensagem.lida = False
					mensagem.save()
			else:
				turma = get_object_or_404(Turma, pk=request.POST.get('turma'))
				alunosTurma = Aluno.objects.filter(turma=turma)
				for aluno in alunosTurma:
					mensagem = Mensagens()
					mensagem.data_envio = datetime.datetime.now()
					mensagem.data_lida = datetime.datetime.now()

					mensagem.assunto = request.POST.get('assunto')
					mensagem.mensagem = request.POST.get('mensagem')
					#alunoDest = get_object_or_404(Aluno, pk=para)
					mensagem.para = aluno.user.user
					mensagem.destinatario = request.user
					mensagem.lida = False
					mensagem.save()
	
		return render_to_response('enviarMensagem.html', locals(), context_instance=RequestContext(request),)
	
	elif request.user.get_profile().role == 'aluno':
		funcionarios = userProfile.objects.filter(Q(role = 'secretaria') | Q(role = 'professor'))
		if request.method == 'POST':
			sendList = request.POST.getlist('funcionario')
			for destinatario in sendList:
				para = get_object_or_404(userProfile, pk=destinatario)
				mensagem = Mensagens()
				mensagem.data_envio = datetime.datetime.now()
				mensagem.data_lida = datetime.datetime.now()
				mensagem.assunto = request.POST.get('assunto')
				mensagem.mensagem = request.POST.get('mensagem')
				mensagem.para = para.user
				mensagem.destinatario = request.user
				mensagem.lida = False
				mensagem.save()

		return render_to_response('enviarMensagemSchool.html', locals(), context_instance=RequestContext(request),)

@login_required
def homeSecretaria(request):
	turmas = Turma.objects.all()
	return render_to_response('starter.html', locals(), context_instance=RequestContext(request),)

@login_required
def turmasSecretaria(request, pk):
	turma = get_object_or_404(Turma, pk=pk)
	alunos = Aluno.objects.filter(turma=turma)
	turmas = Turma.objects.all()
	return render_to_response('alunosList.html', locals(), context_instance=RequestContext(request),)

@login_required
def boletimAlunoSecretaria(request, pk):
	#userByPk = get_object_or_404(User, pk=pk)
	aluno = get_object_or_404(Aluno, pk=pk)
	turma = get_object_or_404(Turma, pk=aluno.turma.pk)
	turmas = Turma.objects.all()

	d = defaultdict(list)

	for m in turma.materia.all():
		pair = [aluno, m.totalNotas(aluno=aluno.pk)]
		d[m].append(pair)

	f = defaultdict(list)

	for m in turma.materia.all():
		pair = [aluno, m.totalFaltas(aluno=aluno.pk)]
		f[m].append(pair)
	
	data = dict(d)
	dataFaltas = dict(f)

	return render_to_response('alunoHome.html', locals(), context_instance=RequestContext(request),)

@login_required
def cadastroAlunos(request):
	formUser = NewUserForm() 
	formAluno = NewAlunoForm()
	if request.method == 'POST':
		usuario = NewUserForm(request.POST)
		usuario.is_active = True
		usuario.is_staff = False
		usuario.is_superuser = False
		usuario.date_joined = datetime.datetime.now()
		usuario.last_login = datetime.datetime.now()
		usuario.save()
		
		user = get_object_or_404(User, username=request.POST.get('username'))
		
		usuarioPerfil = userProfile()
		usuarioPerfil.user = user
		usuarioPerfil.role = 'aluno'
		usuarioPerfil.save()

		profile = get_object_or_404(userProfile, user=user)
		turma = get_object_or_404(Turma, pk=request.POST.get('turma'))
		#aluno = NewAlunoForm(request.POST)
		aluno = Aluno()
		aluno.matricula = request.POST.get('matricula')
		aluno.nomeAluno = request.POST.get('nomeAluno')
		aluno.dataNascimento = request.POST.get('dataNascimento')
		aluno.user = profile
		aluno.turma = turma
		aluno.save()

	return render_to_response('novoAluno.html', locals(), context_instance=RequestContext(request),)

@login_required
def cadastroTurma(request):
	form = NovaTurmaForm()
	if request.method == 'POST':
		form = NovaTurmaForm(request.POST)
		form.save()
		message = 'Turma Cadastrada!'
	return render_to_response('novaTurma.html', locals(), context_instance=RequestContext(request),)


@login_required
def cadastroProfessor(request):
	formUser = NewUserForm() 
	#form = NewProfForm()
	if request.method == 'POST':
		usuario = NewUserForm(request.POST)
		usuario.is_active = True
		usuario.is_staff = False
		usuario.is_superuser = False
		usuario.date_joined = datetime.datetime.now()
		usuario.last_login = datetime.datetime.now()
		usuario.save()
		
		user = get_object_or_404(User, username=request.POST.get('username'))
		
		usuarioPerfil = userProfile()
		usuarioPerfil.user = user
		usuarioPerfil.role = 'professor'
		usuarioPerfil.save()

		profile = get_object_or_404(userProfile, user=user)
		#turma = get_object_or_404(Turma, pk=request.POST.get('turma'))
		prof = Professor()
		prof.nome = '%s %s' % (request.POST.get('first_name'), request.POST.get('last_name'))
		prof.user = profile
		prof.save()

	return render_to_response('novoProfessor.html', locals(), context_instance=RequestContext(request),)

@login_required
def cadastroGrade(request):
	form = NewGradeForm()
	if request.method == 'POST':
		form = NewGradeForm(request.POST)
		form.save()
		message = 'Associação Matéria-Professor criada!'
	return render_to_response('novaGrade.html', locals(), context_instance=RequestContext(request),)