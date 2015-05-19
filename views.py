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
	return render(request, 'content/home.html', context)


# Список категорий (с возможностью редактирования)
def editCategories(request):

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	# Импортируем
	from project.models import Category

	# Получаем дерево категорий
	categories = []
	categories = getCategoryTree(categories)

	# Корректируем имена с учетом вложеннот
	for category in categories:
		category.name = '— ' * category.level + category.name

	context = {'categories': categories}
	return render(request, 'content/categories.html', context)


# Дерево категорий (используется рекурсия)
def getCategoryTree(tree, parent=None):

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	# Импортируем
	from project.models import Category

	# Получаем список дочерних категорий
	categories = Category.objects.filter(parent=parent).order_by('order')

	# Проходим по списку категорий с рекурсивным погружением
	for category in categories:
		tree.append(category)
		tree = getCategoryTree(tree, category)

	# Возвращаем результат
	return tree


# Авторизация пользователя с перенаправлением
def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		redirect_url = request.POST.get('redirect')
		if not redirect_url: redirect_url = '/'
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


# Выход пользователя с перенаправлением
def logout_view(request):
	if request.method == 'POST':
		redirect_url = request.POST.get('redirect')
		if not redirect_url: redirect_url = '/'
		logout(request)
		return redirect(redirect_url)
	else:
		return HttpResponse(status=400)


# Save Article
def ajaxSaveArticle(request):

	# Импортируем
	from project.models import Article
	from django.utils import timezone
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	# TODO Обрабатываем входные данные
	try:
		article = Article.objects.get(id = request.POST.get('article_id'))
	except Article.DoesNotExist:
		article = Article()

	result = {
		'status': 'success',
		'message': 'Входные данные получены'}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# Add Category
def ajaxAddCategory(request):

	# Импортируем
	from project.models import Category
	from django.db.models import Max
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	# Проверяем на пустые значения
	if (request.POST.get('name').strip() == '') or (request.POST.get('parent').strip() == ''):
		result = {'status': 'warning', 'message': 'Пожалуй, вводные данные не корректны.'}
	else:

		name = request.POST.get('name').strip()

		alias = name.lower()
		alias = alias.replace(' ', '-')

		if (request.POST.get('parent').strip() == 'null'):
			parent = None
			level = 0
		else:
			try:
				parent = Category.objects.get(id=request.POST.get('parent').strip())
				level = parent.level + 1
			except Category.DoesNotExist: # Указанная родительская категория не существует
				return HttpResponse(status=406)

		category = Category(name=name, alias=alias, parent=parent, level=level, order=-1, path='', created=datetime.now(), modified=datetime.now())
		category.save()

		if (parent == None):
			category.path = '/' + str(category.id) + '/'
		else:
			category.path = parent.path + str(category.id) + '/'

		category.order = Category.objects.filter(parent=category.parent).aggregate(Max('order'))['order__max'] + 1

		category.save()

		if (parent == None):
			parentId = 'none'
		else:
			parentId = parent.id

		result = {'status': 'success', 'message': 'Категория ' + name + ' добавлена.', 'categoryId': category.id, 'categoryName': category.name, 'categoryAlias': category.alias, 'parentId': parentId}

	# Получаем дерево категорий
	categories = []
	categories = getCategoryTree(categories)

	# Проводим общую нумерацию категорий
	for order, category in enumerate(categories):
		category.order = order
		category.save()

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# Switch Category State
def ajaxSwitchCategoryState(request):

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	# Проверяем корректность вводных данных
	if not request.POST.get('id') or not request.POST.get('state'):
		result = {'status': 'warning', 'message': 'Пожалуй, вводные данные не корректны.'}
	else:
		try:
			category = Category.objects.get(id=request.POST.get('id'))
			if request.POST.get('state') == 'true':
				category.state = True;
			else:
				category.state = False;
			category.save();
			result = {'status': 'success', 'message': 'Статус категории ' + category.name + ' изменен на ' + str(category.state) + '.'}
		except Category.DoesNotExist:
			result = {'status': 'alert', 'message': 'Категория с идентификатором ' + request.POST.get('id') + ' отсутствует в базе.'}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# Save Category
def ajaxSaveCategory(request):

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	if not request.POST.get('id') or not request.POST.get('name') or not request.POST.get('alias') :
		result = {'status': 'warning', 'message': 'Пожалуй, вводные данные не корректны.'}
	else:
		try:
			category = Category.objects.get(id=request.POST.get('id'))
			category.name = request.POST.get('name')
			category.alias = request.POST.get('alias')
			if request.POST.get('description'): category.description = request.POST.get('description')
			category.save()
			result = {'status': 'success', 'message': 'Изменения категории ' + category.name + ' сохранены.'}
		except Category.DoesNotExist:
			result = {'status': 'alert', 'message': 'Категория с идентификатором ' + request.POST.get('id') + ' отсутствует в базе.'}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')


# Trash Category
def ajaxTrashCategory(request):

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# TODO Проверяем права доступа
	#	return HttpResponse(status=403)

	if not request.POST.get('id'):
		result = {'status': 'warning', 'message': 'Пожалуй, вводные данные не корректны.'}
	else:
		try:
			category = Category.objects.get(id=request.POST.get('id'))
			category.delete()
			result = {'status': 'success', 'message': 'Категория удалена.'}
		except Category.DoesNotExist:
			result = {'status': 'alert', 'message': 'Категория с идентификатором ' + request.POST.get('id') + ' отсутствует в базе.'}

	# Возвращаем ответ
	return HttpResponse(json.dumps(result), 'application/javascript')
