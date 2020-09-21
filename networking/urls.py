from django.urls import path
from . import views
from project_colab import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "networking"

urlpatterns = [
    path('search/',views.search,name='search'),
    path('profile/<username>/',views.profile,name='profile'),
    path('friend/<operation>-<usernameone>-<usernametwo>/',views.friend,name='friend'),
    path('project/projectid<project_id>/',views.project_view,name='project_view'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
