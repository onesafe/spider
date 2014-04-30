from django.conf.urls import patterns, include, url
from django.contrib import admin

from app_explore_image import urls as explore_image_urls
from app_index import views as index_views

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', index_views.test),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^images/', include(explore_image_urls))
)
