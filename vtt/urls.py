
from django.urls import include, path
from . import views	

from .views import Files, File_detail

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index,name='home'),
    #path('home/',views.home, name='home'),
    path('home/', views.index,name='home'),
    path('status/',views.stats),
    
    # path('files/',Files.as_view()),

    path('user_files/',views.get_user_file_list),

    path('files_vtt/<str:findex>',views.send_file_for_subtitle, name = 'f_idx_for_srt_cli'),
    path('files_vtt_status/<str:findex>',views.check_status_of_vtt, name = 'f_idx_for_status'),
    path('files_vtt_get/<str:findex>',views.download_file, name = 'f_idx_for_get_srt'),
    

    path('files/<int:pk>',File_detail.as_view()),
    path('up/',views.simple_upload),

    url(r'^login/$', auth_views.LoginView.as_view(template_name="index.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="vtt/logout.html"), name='logout'),
    url(r'^admin/', admin.site.urls),
    # url(r'^signup/$', views.signup, name='signup'),

    path('tes/', views.test),
    path('contact', views.contact,name='contact')
    ]
