from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'project.views.home', name='home'),
	url(r'^catalog/', include('catalog.urls')),
	url(r'^admin/', include(admin.site.urls)),

	# Article
	# ex: /article/58/
	url(r'^article/(?P<article_id>[0-9]+)/$', 'project.views.article', name='article'),
	# ex: /articles/
	url(r'^articles/$', 'project.views.articles', name='articles'),

	# Content Lists
	url(r'^content/categories/$', 'project.views.editCategories', name='editCategories'),

	# Ajax Article
	url(r'^content/ajax/get-article/$', 'project.views.ajaxGetArticle', name='ajaxGetArticle'),
	url(r'^content/ajax/save-article/$', 'project.views.ajaxSaveArticle', name='ajaxSaveArticle'),

	# Ajax Category
	url(r'^content/ajax/add-category/$', 'project.views.ajaxAddCategory', name='ajaxAddCategory'),
	url(r'^content/ajax/save-category/$', 'project.views.ajaxSaveCategory', name='ajaxSaveCategory'),
	url(r'^content/ajax/switch-category-state/$', 'project.views.ajaxSwitchCategoryState', name='ajaxSwitchCategoryState'),
	url(r'^content/ajax/trash-category/$', 'project.views.ajaxTrashCategory', name='ajaxTrashCategory'),


	# ex: /login/
	url(r'^login/$', 'project.views.login_view', name='login_view'),
	url(r'^logout/$', 'project.views.logout_view', name='logout_view'),
)
