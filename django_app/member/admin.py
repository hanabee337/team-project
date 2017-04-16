from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import MyUser


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'img_profile')}),
        (_('Personal info'), {'fields': ('nickname', 'gender', 'age',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    list_display = ('email', 'nickname',)
    list_filter = ('is_staff',)


admin.site.register(MyUser, MyUserAdmin)
