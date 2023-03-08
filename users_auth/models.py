from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import TextField


class Organization(models.Model):
    name = TextField(blank=False)
    domain = TextField(blank=True)


def member_picture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'media/member/{filename}'


class Member(models.Model):
    name = TextField(blank=False)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE,related_name="members")
    picture = models.FileField(upload_to=member_picture_directory_path)


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="members")
    terminal_code = TextField(blank=False)
    date_time = models.DateTimeField(auto_now=True)

# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="users")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
#
