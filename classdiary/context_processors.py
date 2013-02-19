from classdiary.models import *
from school import settings

def messagesCount(request):
	if request.user.is_authenticated():
		m = Mensagens.objects.filter(para=request.user)
		m = m.filter(lida=False).count()
		return { 'novasMensagens' : m, }
	else:
		return { 'novasMensagens' : None, }