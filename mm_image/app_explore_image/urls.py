from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # url(r'^$', views.test),
    url(r'(?P<catagory>\w+)$', views.test),
)