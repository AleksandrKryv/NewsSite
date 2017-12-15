from django.contrib import admin
from .models import *


def set_category_status_true(modeladmin, request, queryset):
    queryset.update(is_active=True)

set_category_status_true.short_description = 'Switch category active status to True'


def set_category_status_false(modeladmin, request, queryset):
    queryset.update(is_active=False)

set_category_status_false.short_description = 'Switch category active status to False'


def set_post_is_approve_status_true(modeladmin, request, queryset):
    queryset.update(is_approved=True)

set_post_is_approve_status_true.short_description = 'switch approve status to True '


def set_post_is_approve_status_false(modeladmin, request, queryset):
    queryset.update(is_approved=False)

set_post_is_approve_status_false.short_description = 'switch approve status to False '


class NSuserAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'is_active')
    actions = [set_category_status_false, set_category_status_true]


class NewsPostAdmin(admin.ModelAdmin):

    def can_pub(self):
        return self.is_approved

    can_pub.boolean = True
    can_pub.short_description = "Can publish"
    list_display = ('post_header', 'post_category', 'is_approved', can_pub,)
    readonly_fields = ('post_source', 'post_photo')

    actions = [set_post_is_approve_status_false, set_post_is_approve_status_true]


class CommentAdmin(admin.ModelAdmin):
    pass


class IsReadByUserStatusAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(IsReadByUserStatus, IsReadByUserStatusAdmin)
admin.site.register(NSuser, NSuserAdmin)
admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)