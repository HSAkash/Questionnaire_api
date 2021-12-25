from django.contrib import admin
from post import models


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'published_date')
    list_filter = ('published_date',)
    search_fields = ('title', 'user')
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    filter_horizontal = ()
    fieldsets = ()
    list_per_page = 10


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user')
    search_fields = ('question', 'user')
    filter_horizontal = ()
    fieldsets = ()
    list_per_page = 10


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
