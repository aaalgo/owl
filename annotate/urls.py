from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.anno, name='anno'),
    url(r'^log$', views.log, name='log'),
    url(r'^review/([0-9]+)$', views.review, name='review'),
    url(r'^image/([0-9]+)\.png$', views.image, name='image'),
]

