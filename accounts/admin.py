from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('id', 'user_id', 'email', 'full_name', 'admin','email_verified')
    list_filter = ('admin', 'staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'full_name','fcm_token','is_online', 'email_token', 'otp_code', 'user_type', 'availability_interval', 'email_verified', 'location_name','lat','lng', 'password')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
