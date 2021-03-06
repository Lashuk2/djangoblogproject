from django.contrib import admin
from blog.models import Post, PostCountView, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'post', 'created_on', 'active')
    list_filter = ('created_on', 'active')
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Comment, CommentAdmin)


class PostCountViewAdmin(admin.ModelAdmin):
    list_display = ('sesId', 'postId')
    list_filter = ('postId',)
    search_fields = ['postId']


admin.site.register(PostCountView, PostCountViewAdmin)
