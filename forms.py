# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, ModelChoiceField, ChoiceField
from django.contrib.localflavor.br.forms import *
#from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import *
#from django.contrib.admin import widgets

from classdiary.models import *

class NotasForm(forms.ModelForm):
    
    class Meta:
        model = DiarioNotas
        exclude = ('aluno','materia')

class NewUserForm(forms.ModelForm):

	class Meta:
		model = User
		exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups','user_permissions')

class NewAlunoForm(forms.ModelForm):

	class Meta:
		model = Aluno
		exclude = ('user')

class NewGradeForm(forms.ModelForm):

	class Meta:
		model = Grade
		#exclude = ('user')		

class NovaTurmaForm(forms.ModelForm):

	class Meta:
		model = Turma
		#exclude = ('user')