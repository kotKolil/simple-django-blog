from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import *
from blog import views
from blog import forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static





handler404 = "blog.views.pnf"

api = [
    path('comment/', views.comment_api),
    path('state/', views.view_state_api),
]

urlpatterns = [

    path('admin/', admin.site.urls),
    path("",views.main),
    path("ish_kab/", views.ish_kab), 
    path('set_channel/' , views.set_channel),
    path('studio/' , views.studio),
    path('new_state/' , views.create_new_state),
    path("state/" , views.view_state),
    path('popular/' , views.states_list),
    path('channels/' , views.all_channel),
    path('channel/' , views.channel),
    path('api/' , include(api)),
    path('post_comment/', views.post_comment),
    path("upload_image/", views.up_img),
    path("del_state/", views.del_state),


    #authentication system
    path("reg/", views.reg),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)