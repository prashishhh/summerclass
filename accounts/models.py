from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ------------------------
# Custom User Manager
# ------------------------
class MyAccountManager(BaseUserManager):
    # Create normal user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    # Create superuser
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# ------------------------
# Custom User Model
# ------------------------
class Account(AbstractBaseUser, PermissionsMixin):


    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

    STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('banned', 'Banned'),
]

    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True)

    # Optional fields
    gender = models.CharField(
        max_length=1,
        choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('active', 'Active')),
        default='pending'
    )

    profile_picture = models.ImageField(upload_to='photos/profiles/', blank=True, null=True) 

    # Required fields
    date_joined  = models.DateTimeField(auto_now_add=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Authentication setup
    USERNAME_FIELD = 'email'       # login with email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Connect to custom manager
    objects = MyAccountManager()

    # String representation
    def __str__(self):
        return self.email

    # Permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # Utility
    def get_full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.email
