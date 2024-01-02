from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'datetime_created', 'datetime_modified',)
    ordering = ('-datetime_created',)

# admin.site.register(Post, PostAdmin)
