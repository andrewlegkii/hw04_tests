from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели в интерфейсе админки."""

    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели в интерфейсе админки."""

    list_display = ('pk', 'title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
