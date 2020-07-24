from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self,email,password,user_role):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.usr_role = user_role
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,*args,**kwargs):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.usr_role = 'Admin'
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    active = models.BooleanField(default=True)
    staff = models.BooleanField()
    admin = models.BooleanField(default=False)
    usr_role = models.CharField(max_length=30,default='')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usr_role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def user_role(self):
        return self.usr_role

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mob_num = models.CharField(max_length=10)
    adderss = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=150)
    pincode = models.CharField(max_length=20)


