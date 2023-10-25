from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from restaurant.models import Cooker, Dish, DishType


@admin.register(Cooker)
class CookerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    list_filter = ("username", )
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("years_of_experience",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name", "years_of_experience",)}),
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "dish_type")


@admin.register(DishType)
class DishTypeAdmins(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display
