from django.contrib import admin
from .models import Post, Comment


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'status')
    list_filter = ('publish', 'author')
    # search field showing at admin panel for fields
    search_fields = ('title', 'body')
    # autofullfill slug when adding title
    prepopulated_fields = {'slug': ('title',)}
    # adding near field Author models of authors
    raw_id_fields = ('author',)
    # under seach field, buttons with dates
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('created', 'active', 'post')
    search_fields = ('email', 'name', 'body')
