from django.contrib import admin
from .models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'datecompleted', 'important')
    list_filter = ('important',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

    readonly_fields = ('created_at',)



admin.site.register(Task, TaskAdmin)

