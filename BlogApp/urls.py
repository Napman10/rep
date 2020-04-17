from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('registration', views.user_fill, name='registration'),
    path('profile', views.profile, name='profile'),
    path('writenote', views.writenote, name='writenote'),
    path('editme', views.editme, name='editme'),
    path('editstatus', views.editstatus, name='editstatus'),
    path('editnote', views.editnote, name='editnote'),
    path('deletenote', views.deletenote, name='deletenote'),
    path('editimage', views.editimage, name='editimage'),
    path('delimage', views.delimage, name='delimage'),
] 