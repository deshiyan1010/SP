from django.urls import path
from . import views
from project_colab import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "project_management"

urlpatterns = [
    path('project_creation/',views.project_creation,name='project_creation'),
    path('project_application/<project_id>/',views.project_application,name='project_application'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()