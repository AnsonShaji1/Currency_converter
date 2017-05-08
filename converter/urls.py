from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.login_view,name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^register/',views.register_view,name='register'),
    url(r'^first_page/',views.first_page,name='first'),
    url(r'^calculations/$',views.calculations,name='calculations'),
]