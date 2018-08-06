from django.conf.urls import url
from . import views           
urlpatterns = [
url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'), 
url(r'^fave/(?P<id>\d+)$', views.faveorite, name='faveorite'), 
url(r'^user/(?P<id>\d+)$', views.user, name='user'),
url(r'^add$', views.add, name='add'),
url(r'^logout$', views.logout, name='logout'),
url(r'^$', views.quotes, name='quotes'),

]