from django.contrib import admin
from .models import Follower

# connect Post with PostAdmin, which inherits everything from admin.ModelAdmin
class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower, FollowerAdmin)