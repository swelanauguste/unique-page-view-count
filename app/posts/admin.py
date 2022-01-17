from django.contrib import admin

from .models import Post, IPAddress

admin.site.register(Post)
admin.site.register(IPAddress)
