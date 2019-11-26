from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models




class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None

    fio = models.CharField('ФИО', max_length=50, blank=True, null=True, default='не указано')
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.EmailField('Эл. почта', unique=True)
    # town = models.ForeignKey(Town, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Город')
    avatar = models.ImageField('Фото', upload_to='ava_img/', blank=True)
    info = models.TextField('О себе', blank=True, null=True, default='не указано')
    profession = models.CharField('Профессия', max_length=50, blank=True, null=True, default='не указано')
    hobby = models.CharField('Хобби', max_length=50, blank=True, null=True, default='не указано')
    study = models.CharField('Образование', max_length=50, blank=True, null=True, default='не указано')
    isOfferRent = models.BooleanField('Арендадатель?', default=False)
    profile_ok = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_avatar(self):
        if not self.avatar:
            return 'http://placehold.it/200'
        else:
            return self.avatar.url



