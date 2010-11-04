from blog.models import Entry, Comment
from django.contrib import admin

class CommentAdmin(admin.TabularInline):
    ordering = ['-created']
    list_display = ('content',)
    model = Comment

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'esta_publicado')
    inlines = [CommentAdmin]

class CommentAdmin2(admin.ModelAdmin):
    ordering = ['-created']

admin.site.register(Entry,EntryAdmin)
admin.site.register(Comment,CommentAdmin2)
