from django.conf.urls import url,include
from zumaInfo import views

from zumaInfo.views import TrabajadorList,get_trabajador_authenticated
from zumaInfo.views import ClienteList,get_cliente_authenticated

from rest_framework import routers
from rest_framework.authtoken import views as rest_views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/trabajador/$', TrabajadorList.as_view()),
    url(r'^api/cliente/$', ClienteList.as_view()),
    url(r'^api/trabajador/authenticated/$', get_trabajador_authenticated),
    url(r'^api/cliente/authenticated/$', get_cliente_authenticated),
    url(r'^api/token-auth/', rest_views.obtain_auth_token),
    url(r'^api/', include(router.urls)),

    url(r'^api/user/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^api/categoria/(?P<nombre>[\w\-]+)/$', views.categoria_detail),
    url(r'^api/interes/(?P<nombre>[\w\-]+)/$', views.interes_detail),

    #url(r'^api/cliente/solicitud/(?P<username>[\w\-]+)/$', views.solicitud_cliente),
    url(r'^api/usuario/tipo/$', views.tipo_usuario),
    url(r'^api/cliente/solicitud/$', views.solicitud_cliente),
    url(r'^api/trabajador/solicitud/$', views.solicitud_trabajador),
    url(r'^api/trabajador/interes/(?P<nombre>[\w\ ]+)/$', views.solicitud_trabajador_interes),
    url(r'^api/solicitud/$', views.create_solicitud),

]
