from django.urls import path
from . import views
from project_colab import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "posts"

urlpatterns = [
    path('home/',views.home,name='home'),
    path('delete-comment/<int:post_id>/',views.delete_post,name='delete_post'),
    path('delete-comment/<int:post_id>-<int:comment_id>/',views.delete_comment,name='delete_comment'),
    path('like/<int:post_id>',views.like,name='like'),
    path('dislike/<int:post_id>',views.dislike,name='dislike'),
    path('post_edit/<int:post_id>',views.editpost,name='editpost'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
