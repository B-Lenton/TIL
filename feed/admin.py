from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
