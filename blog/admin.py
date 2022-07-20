from django.contrib import admin
from django.utils.translation import ngettext
from django.contrib import messages

from .models import Article, Category

# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')


admin.site.site_header = 'وبلاگ جنگویی'
admin.site.disable_action('delete_selected')
# @admin.action(description='Mark selected stories as published')
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d مقاله منتشر شد.',
        '%d مقاله منتشر شدند.',
        updated,
    ) % updated, messages.SUCCESS)


def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d عدد از مقالات تغییر یافت',
        '%d عدد از مقالات تغییر یافتند',
        updated
    ) % updated, messages.SUCCESS)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'jalali_published', 'category_to_str']
    list_editable = ['status']
    list_filter = ['status']
    search_fields = ['title', 'status']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['created']

    actions = [make_published, make_draft]
    make_published.short_description = 'منتشر کردن'
    make_draft.short_description = 'پیش نویس کردن'

    def category_to_str(self, obj):
        return ', '.join([category.title for category in obj.category_published()])

    category_to_str.short_description = 'دسته بندی ها'






@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position', 'title', 'slug', 'parent', 'status']
    list_editable = ['status']
    list_filter = (['status'])
    search_fields = ['slug', 'status']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-parent']





