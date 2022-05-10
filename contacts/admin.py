from csv import list_dialects

from django.contrib import admin

# Register your models here.
from .models import Category, Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'phone', 'email', 'creation_date', 'category')
    list_display_links = ('name', 'last_name')
    #list_filter = ('name', 'last_name')
    list_per_page = 5
    search_fields = ('name', 'last_name', 'phone')

admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
