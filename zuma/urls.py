from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    #url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('zumaInfo.urls')),

]
