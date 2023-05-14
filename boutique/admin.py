from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Category, Size, Address, Supplier, Item, ItemSize, Purchase, Employee, Warehouse, Sales, User, Stock


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the models
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Address)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(ItemSize)
admin.site.register(Purchase)
admin.site.register(Employee)
admin.site.register(Warehouse)
admin.site.register(Sales)
admin.site.register(Stock)
admin.site.register(User, CustomUserAdmin)
