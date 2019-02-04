from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views
# Eğer viewset değil APIView kullanıyorsak default router kullanamayız.
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, base_name='login')
# Bir model viewset register ederken base_name belirtmek zorunda değilim, çünkü
# Django rest framework modelde serializer a kayıtlı olup viewset imize kayıtlı
# olanlara bakarak otomatik olarak algılıyor.
router.register('feed', views.UserProfileFeedViewSet)
urlpatterns = [
    url(r'^hello-view/', views.HelloApiView.as_view()),
    url(r'', include(router.urls)) # Bu şekilde router object bizim için router
    # da register ettiğimiz url leri create ediyor. include da onları ekliyor.
    # r den sonra blank string '' bırakmamızın sebebi ise django'dan herhangi
    # bir url ile eşleşmezse router ımızı feed edicek, böylece ilk yazdığımız
    # (12.satırdaki) url pattern ini kontrol edecek eğer orda birşeyle eşleşmez
    # ise o zaman router dakileri kontrol edecek.

]
