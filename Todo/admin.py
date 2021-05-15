from django.contrib import admin
from .models import Todo

# Register your models here.
from Todo.models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)  # It is created the Date or time in the Admin channel which cannot be changed


admin.site.register(Todo, TodoAdmin)
