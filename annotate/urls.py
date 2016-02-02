from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.anno, name='anno'),
    url(r'^log$', views.log, name='log'),
    url(r'^image/([0-9]+)$', views.image, name='image'),
]

