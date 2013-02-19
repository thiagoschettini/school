from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'classdiary.views.home', name='home'),
    url(r'^professor/$', 'classdiary.views.homeProfessor', name='home_professor'),
    url(r'^secretaria/$', 'classdiary.views.homeSecretaria', name='home_secretaria'),
    url(r'^aluno/$', 'classdiary.views.homeAluno', name='home_aluno'),
    url(r'^boletim/$', 'classdiary.views.boletimAluno', name='boletim_aluno'),

    url(r'^(?P<pk>[0-9]+)/boletim/$', 'classdiary.views.boletimAlunoSecretaria', name='boletim_aluno_secretaria'),

    url(r'^aluno/novo/$', 'classdiary.views.cadastroAlunos', name='novo_aluno'),

    url(r'^professor/novo/$', 'classdiary.views.cadastroProfessor', name='novo_professor'),

    url(r'^professor/materia/$', 'classdiary.views.cadastroGrade', name='nova_grade'),

    url(r'^turma/nova/$', 'classdiary.views.cadastroTurma', name='nova_turma'),

    url(r'^(?P<pk>[0-9]+)/alunos/$', 'classdiary.views.turmasSecretaria', name='alunos_turma'),

    url(r'^enviar/mensagem/$', 'classdiary.views.mensagem', name='enviar_mensagem'),
    url(r'^ver/mensagem/$', 'classdiary.views.mensagemLista', name='ver_mensagens'),
    url(r'^minhas/mensagem/$', 'classdiary.views.minhasMensagens', name='ver_minhas_mensagens'),

    url(r'^mensagem/(?P<pk>[0-9]+)/$', 'classdiary.views.mensagemDetalhe', name='detalhe_mensagem'),
    url(r'^aluno/by/turma/(?P<pk>[0-9]+)/$', 'classdiary.views.mensagemAlunos', name='alunos_byTurma'),
    #url(r'^prof/$', 'classdiary.views.adminView', name='admin_prof'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^(?P<pk>[0-9]+)/edit/$', 'classdiary.views.turmaView', name='diario_turma'),
    url(r'^(?P<pk>[0-9]+)/diario/(?P<filtro>[\w_-]+)$', 'classdiary.views.alunoView', name='diario_aluno'),

    url(r'^(?P<pk>[0-9]+)/edit/nota$', 'classdiary.views.editNota', name='diario_edit_nota'),
    url(r'^(?P<pk>[0-9]+)/edit/falta$', 'classdiary.views.editFalta', name='diario_edit_falta'),
    # url(r'^school/', include('school.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^eventos/', include('schedule.urls')),
)

urlpatterns += patterns('django.views.static',
    (r'^web/$', 
        'serve', {
        'document_root': '/Users/thiagoschettini/code/school/web/',
        'show_indexes': True }),)