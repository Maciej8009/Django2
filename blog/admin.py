from django.contrib import admin
from .models import Post, CommentsPost

admin.site.register(Post)
admin.site.register(CommentsPost)