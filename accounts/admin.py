from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomizedUser
from accounts.forms import UserCreationForm, UserChangeForm


@admin.register(CustomizedUser)
class CustomizedUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
    'username', 'email', 'vk_page', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Personal info', {'fields': ('vk_page', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),
    )
    readonly_fields = ('username', 'email')

    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'vk_page', 'date_of_birth', 'password1',
            'password2')}
         ),
    )
    add_readonly_fields = ()

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.add_readonly_fields
        return self.readonly_fields


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
