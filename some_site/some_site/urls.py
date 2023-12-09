"""
URL configuration for some_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from blog import views
from django.conf import settings
from django.conf.urls.static import static



handler404 = "blog.views.pnf"

api = [
    path('comment_api/', views.comment_api, name='comment_api'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.main),
    path('reg/' , views.reg),
    path('reg/get_reg/' , views.get_reg),
    path("auth/" , views.auth),
    path("auth/get_auth/" , views.get_auth),
    path("logout/", views.lg),
    path("ish_kab/", views.ish_kab), 
    path('set_channel/' , views.set_channel),
    path('set_channel/get_new_channel/' , views.get_new_channel),
    path('studio/' , views.studio),
    path('new_state/' , views.create_new_state),
    path("new_state/get_new_state/", views.get_new_state),
    path("state/" , views.view_state),
    path('popular/' , views.states_list),
    path('channels/' , views.all_channel),
    path('channel/' , views.channel),
    path('api/' , include(api)),
    path('post_comment/', views.post_comment),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += url(r'',include('users.urls'))
