from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout

# Главная страница
def home(request):
#	updaters_list = Updater.objects.all()
	test = 'test'
	context = {'test': test}
	return render(request, 'project/home.html', context)

def login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	redirect = request.POST.get('redirect')
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			return HttpResponse(status=404)
		else:
			return HttpResponse(status=402)
	else:
		return HttpResponse(status=403)

def logout_view(request):
	logout(request)
	# Redirect to a success page.
