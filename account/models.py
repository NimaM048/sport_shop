from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self,phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone=self.normalize_email(phone),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,
        null= True,
        blank=True,
        unique=True,
    )
    biography = models.TextField(null=True, blank=True)
    fullname = models.CharField(max_length=50 , verbose_name="نام کامل")
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, unique=True, verbose_name="شماره تلفن")
    is_admin = models.BooleanField(default=False, verbose_name="ادمین")
    birthday_date = models.IntegerField(null= True, blank=True)
    web_site = models.CharField(max_length=100,null= True, blank=True)
    github = models.CharField(max_length=100,null= True, blank=True)
    linkdin = models.CharField(max_length=100,null= True, blank=True)
    telegram = models.CharField(max_length=100,null= True, blank=True)
    profile_picture = models.FileField(upload_to='profile_pictures/', null=True, blank=True,
                                        verbose_name="عکس پروفایل")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.fullname

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










class Otp(models.Model):
    token = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    exprision_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Add this field




    def __str__(self):
        return self.phone





class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.fullname} - {self.ip_address}"











class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    read = models.BooleanField(default=False, verbose_name='خوانده شده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اطلاعیه'
        verbose_name_plural = 'اطلاعیه‌ها'