from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_date", "published_date")
    list_filter = ("status", "created_date", "published_date", "author", "categories")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_date"
    ordering = ("-created_date",)
