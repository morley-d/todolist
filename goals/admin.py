from django.contrib import admin

from goals.models import Category, Comment, Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, GoalCategoryAdmin)
admin.site.register(Goal)
admin.site.register(Comment)
