from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Главная страница
def home(request):
#	updaters_list = Updater.objects.all()
	test = 'test'
	context = {'test': test}
	return render(request, 'project/home.html', context)

def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		redirect_url = request.POST.get('redirect')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(redirect_url)
			else:
				# TODO Сделать человечный ответ
				# Пользователь заблокирован
				return HttpResponse(status=401)
		else:
			# TODO Сделать человечный ответ
			# Пользователь неавторизован
			return HttpResponse(status=401)
	else:
		return HttpResponse(status=400)

def logout_view(request):
	if request.method == 'POST':
		redirect_url = request.POST.get('redirect')
		logout(request)
		return redirect(redirect_url)
	else:
		return HttpResponse(status=400)

