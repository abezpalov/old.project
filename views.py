from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout


def home(request):
	"Представление: Главная страница."

	return render(request, 'content/home.html', locals())


def editArticles(request):
	"Представление: Список статей (с возможностью редактирования)."

	# Импортируем
	from project.models import Article, Category, Language

	# Проверяем права доступа
	if request.user.has_perm('project.change_article'):

		# Получаем списки объектов
		articles   = Article.objects.all().order_by('-created')
		categories = []
		categories = getCategoryTree(categories)
		for category in categories:
			category.name = '— ' * category.level + category.name
		languages  = Language.objects.all()

	return render(request, 'content/edit-articles.html', locals())


def editCategories(request):
	"Представление: Список категорий (с возможностью редактирования)."

	# Проверяем права доступа
	if request.user.has_perm('project.change_category'):

		# Импортируем
		from project.models import Category

		# Получаем дерево категорий
		categories = []
		categories = getCategoryTree(categories)
		for category in categories:
			category.name = '— ' * category.level + category.name

	return render(request, 'content/edit-categories.html', locals())


def getCategoryTree(tree, parent=None):
	"Функция: Дерево категорий (используется рекурсия)."

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


def login_view(request):
	"Представление: Авторизация пользователя с перенаправлением."

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


def logout_view(request):
	"Представление: Выход пользователя с перенаправлением."

	if request.method == 'POST':
		redirect_url = request.POST.get('redirect')
		if not redirect_url: redirect_url = '/'
		logout(request)
		return redirect(redirect_url)
	else:
		return HttpResponse(status=400)


def ajaxGetArticle(request):
	"AJAX-представление: Получение статьи."

	# Импортируем
	import json
	from project.models import Article

	# Проверяем права доступа
	if not request.user.has_perm('project.change_article'):
		return HttpResponse(status=403)

	# Получаем объект
	try:
		article = Article.objects.get(id = request.POST.get('id'))

		# Проверяем
		if article.category: article_category_id = article.category.id
		else: article_category_id = 0
		if article.language: article_language_id = article.language.id
		else: article_language_id = 0

		result = {
			'status': 'success',
			'message': 'Данные продукта получены.',
			'article_id': article.id,
			'article_title': article.title,
			'article_content': article.content,
			'article_alias': article.alias,
			'article_patch': article.patch,
			'article_thumb_src': article.thumb_src,
			'article_intro': article.intro,
			'article_description': article.description,
			'article_category_id': article_category_id,
			'article_language_id': article_language_id,
			'article_source': article.source,
			'article_source_url': article.source_url,
			'article_state': article.state,
			'article_on_main': article.on_main}

	except Article.DoesNotExist:
		result = {
			'status': 'alert',
			'message': 'Ошибка: статья отсутствует в базе.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxSaveArticle(request):
	"AJAX-представление: Сохранение статьи."

	# Импортируем
	import json
	from django.utils import timezone
	from project.models import Article, Category, Language

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	try:
		article = Article.objects.get(id = request.POST.get('id'))
		if not request.user.has_perm('project.change_article'):
			return HttpResponse(status=403)
	except Article.DoesNotExist:
		article = Article()
		if not request.user.has_perm('project.add_article'):
			return HttpResponse(status=403)
		article.created = timezone.now()
		article.created_by = "{} {}".format(request.user.first_name, request.user.last_name)

	# title
	if not request.POST.get('article_title').strip():
		result = {
			'status': 'alert',
			'message': 'Ошибка: отсутствует заголовок.'}
		return HttpResponse(json.dumps(result), 'application/javascript')
	article.title   = request.POST.get('article_title').strip()[:100]

	# content
	if not request.POST.get('article_content').strip():
		result = {
			'status': 'alert',
			'message': 'Ошибка: отсутствует содержание статьи.'}
		return HttpResponse(json.dumps(result), 'application/javascript')
	article.content = request.POST.get('article_content').strip()

	# alias
	if request.POST.get('article_alias').strip():
		article.alias = request.POST.get('article_alias').strip()[:100]

	# patch
	if request.POST.get('article_patch').strip():
		article.patch = request.POST.get('article_patch').strip()[:512]

	# thumb_src
	if request.POST.get('article_thumb_src').strip():
		article.thumb_src = request.POST.get('article_thumb_src').strip()[:512]

	# intro
	if request.POST.get('article_intro').strip():
		article.intro = request.POST.get('article_intro').strip()
	else:
		article.intro = request.POST.get('article_content').strip()[:42]

	# description
	if request.POST.get('article_description').strip():
		article.intro = request.POST.get('article_description').strip()
	else:
		article.intro = ''

	# category
	try:
		article.category = Category.objects.get(id = request.POST.get('article_category_id'))
	except Category.DoesNotExist:
		article.category = None

	# language
	try:
		article.language = Language.objects.get(id = request.POST.get('article_language_id'))
	except Language.DoesNotExist:
		article.language = None

	# source
	if request.POST.get('article_source').strip():
		article.source = request.POST.get('article_source').strip()[:512]

	# source_url
	if request.POST.get('article_source_url').strip():
		article.source_url = request.POST.get('article_source_url').strip()[:512]

	# state
	if request.POST.get('article_state') == 'true':
		article.state = True
	else:
		article.state = False

	# on_main
	if request.POST.get('article_on_main') == 'true':
		article.on_main = True
	else:
		article.on_main = False

	# modified
	article.modified = timezone.now()
	article.modified_by = "{} {}".format(request.user.first_name, request.user.last_name)

	# published
	if article.state:
		article.published = timezone.now()
		article.published_by = "{} {}".format(request.user.first_name, request.user.last_name)

	# Сохраняем статью
	article.save()

	# Возвращаем ответ
	result = {
		'status': 'success',
		'message': 'Статья сохранена.'}

	return HttpResponse(json.dumps(result), 'application/javascript')


def ajaxAddCategory(request):
	"AJAX-представление: Добавление категории."

	# Импортируем
	from project.models import Category
	from django.db.models import Max
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('project.change_category'):
		return HttpResponse(status=403)

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


def ajaxSwitchCategoryState(request):
	"AJAX-представление: Изменение статуса категории."

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('project.change_category'):
		return HttpResponse(status=403)

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


def ajaxSaveCategory(request):
	"AJAX-представление: Сохранение категории."

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('project.change_category'):
		return HttpResponse(status=403)

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


def ajaxTrashCategory(request):
	"AJAX-представление: Удаление категории."

	# Импортируем
	from project.models import Category
	from datetime import datetime
	import json

	# Проверяем тип запроса
	if (not request.is_ajax()) or (request.method != 'POST'):
		return HttpResponse(status=400)

	# Проверяем права доступа
	if not request.user.has_perm('project.change_category'):
		return HttpResponse(status=403)

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
