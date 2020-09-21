from django.contrib import admin
from posts.models import *


admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Like)
