from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    company_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Role(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    permissions = models.ManyToManyField('auth.Permission', blank=True)



class MyUserManager(BaseUserManager):
    def create_user(self, email, name, company, tc, password=None, password2=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not company:
            raise ValueError("Users must be associated with a company")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            company=company,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, company, tc, password=None):
        user = self.create_user(
            email=email,
            name=name,
            company=company,
            tc=tc,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)  # Use the ID of your default company
    tc = models.BooleanField()
    roles = models.ManyToManyField(Role, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_company_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "company", "tc"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class ProfileUpdate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Date_of_Birth = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='auth/media')
    pan_number = models.CharField(max_length=50)
    pan_picture = models.ImageField(upload_to='auth/media')


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    can_authenticate = models.BooleanField(default=False)  # Whether this user can authenticate other users

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
