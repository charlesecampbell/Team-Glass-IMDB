from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ApplicationUser, Movie, MovieReview, Actor
# Register your models here.
class CustomAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('display_name',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('display_name',)}),
    )
    
admin.site.register(ApplicationUser, CustomAdmin)
admin.site.register(Movie)
admin.site.register(MovieReview)
admin.site.register(Actor)