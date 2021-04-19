from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ApplicationUser, Comment_model, LikedMoviesModel
from .models import WantToSeeModel, HaveSeenModel


# Register your models here.
class CustomAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('display_name', 'bio', 'user_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('display_name', 'bio', 'user_image')}),
    )


admin.site.register(ApplicationUser, CustomAdmin)
admin.site.register(Comment_model)
admin.site.register(LikedMoviesModel)
admin.site.register(WantToSeeModel)
admin.site.register(HaveSeenModel)
