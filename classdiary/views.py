# Create your views here
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import Context, loader, RequestContext

from models import *
from school import settings

def firstView(request):
	alunos = Aluno.objects.all()
	turmas = Turma.objects.all()
	return render_to_response('starter.html', locals(), context_instance=RequestContext(request),)