from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # url(r'^$', views.test),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './templates/js/'} ),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './templates/css/'} ),
    url(r'^qingliang/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/qingliang/'}),
    url(r'^jingyan/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/jingyan/'}),
    url(r'^luoli/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/luoli/'}),
    url(r'^suren/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/suren/'}),
    url(r'^bagua/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/bagua/'}),
    url(r'^cars/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './images/cars/'}),
    url(r'^$', views.error),
    url(r'^praise/$', views.praise),
    url(r'^step/$', views.step),
    url(r'(?P<catagory>\w+)$', views.get_cover, name='catagory'),
)