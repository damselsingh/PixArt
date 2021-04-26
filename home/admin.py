from django.contrib import admin
from .models import People
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('id', 'name','image', 'date', 'user')


admin.site.register(People, UserAdmin)