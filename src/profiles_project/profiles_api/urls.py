from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')

urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'', include(router.urls)) # Bu şekilde router object bizim için router
    # da register ettiğimiz url leri create ediyor. include da onları ekliyor.
    # r den sonra blank string '' bırakmamızın sebebi ise django'dan herhangi
    # bir url ile eşleşmezse router ımızı feed edicek, böylece ilk yazdığımız
    # (12.satırdaki) url pattern ini kontrol edecek eğer orda birşeyle eşleşmez
    # ise o zaman router dakileri kontrol edecek.
]
