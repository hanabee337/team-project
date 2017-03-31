from django.conf.urls import url
from member import views

urlpatterns = [
    url(r'^signup/$', views.SignUp_cbv.as_view(), name='signup'),
]
