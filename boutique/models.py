
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from boutique.constants import ROLES
# from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
# from .admin import CustomUserAdmin
from datetime import date
current_date = date.today()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = CustomUserManager()

    def has_role(self, *roles):
        return self.role in roles

    def is_admin(self):
        return self.has_role('admin')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='boutique_users',  # Add related name for reverse accessor
        related_query_name='boutique_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='boutique_users',  # Add related name for reverse accessor
        related_query_name='boutique_user',
    )
class Size(models.Model):
    size_id = models.CharField(primary_key=True, max_length=5)
    size_name = models.CharField(max_length=10)

    def __str__(self):
        return self.size_name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    subcity = models.CharField(max_length=20)
    woreda = models.CharField(max_length=2)
    house_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.subcity}, Woreda {self.woreda}, House No. {self.house_no}"

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.supplier_name

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    imageurl = models.CharField(max_length=300, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.item_name

    
class ItemSize(models.Model):
    item_size_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.item_name} - {self.size.size_name}"

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_fname = models.CharField(max_length=20)
    employee_lname = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee_fname
    
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    purchase_date = models.DateField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.item_name}, {self.quantity}"

class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.warehouse_id}"

class Sales(models.Model):
    sales_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sales_date = models.DateField(default=current_date)
    quantity = models.IntegerField()
    # seller = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item}"
        # return f"{self.item.item_name} ({self.seller.employee_fname})"

    def get_total_price(self, quantity=1):
        total_price = self.item.price * self.quantity
        return total_price







