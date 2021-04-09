from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ApplicationUser, Comment_model
# Register your models here.
class CustomAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('display_name','likes','want_to_see','have_seen')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('display_name','likes','want_to_see','have_seen')}),
    )
    
admin.site.register(ApplicationUser, CustomAdmin)
admin.site.register(Comment_model)
