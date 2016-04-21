from django.conf.urls import patterns, include, url
from django.contrib import admin

import project.views

admin.autodiscover()

urlpatterns = [

	url(r'^$', project.views.home),
	url(r'^catalog/', include('catalog.urls')),
	url(r'^tenders/', include('tenders.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^articles/$', project.views.articles),
	url(r'^article/(?P<article_id>[0-9]+)/$', project.views.article),

	url(r'^content/ajax/get-article/$', project.views.ajaxGetArticle),
	url(r'^content/ajax/save-article/$', project.views.ajaxSaveArticle),

	url(r'^content/categories/$', project.views.editCategories),

	url(r'^content/ajax/add-category/$', project.views.ajaxAddCategory),
	url(r'^content/ajax/save-category/$', project.views.ajaxSaveCategory),
	url(r'^content/ajax/switch-category-state/$', project.views.ajaxSwitchCategoryState),
	url(r'^content/ajax/trash-category/$', project.views.ajaxTrashCategory),

	url(r'^logs/$', project.views.logs),

	url(r'^login/$', project.views.login_view),
	url(r'^logout/$', project.views.logout_view),
	url(r'^register/$', project.views.register),

]
