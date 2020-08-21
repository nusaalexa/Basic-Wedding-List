from django.contrib import admin

from .models import Gift, GiftList


@admin.register(GiftList)
class GiftListAdmin(admin.ModelAdmin):
    list_display = ['list_name', 'id', 'created_date', 'updated_at']


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'price', 'stock', 'added_date']
