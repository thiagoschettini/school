from django.contrib import admin
from classdiary.models import *

class GradeAdmin(admin.ModelAdmin):
	pass

class SerieAdmin(admin.ModelAdmin):
	pass

class NomeSalaAdmin(admin.ModelAdmin):
	pass

class TurmaAdmin(admin.ModelAdmin):
	pass
	
class AlunoAdmin(admin.ModelAdmin):
	pass
	
class ProfessorAdmin(admin.ModelAdmin):
	pass

class DiarioNotasAdmin(admin.ModelAdmin):
	pass

class DiarioFaltasAdmin(admin.ModelAdmin):
	pass

admin.site.register(Grade, GradeAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(NomeSala, NomeSalaAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(DiarioNotas, DiarioNotasAdmin)
admin.site.register(DiarioFaltas, DiarioFaltasAdmin)
