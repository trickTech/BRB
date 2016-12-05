from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, yiban_uid, nickname):
        if not yiban_uid:
            raise ValueError("易班id不能为空")

        user = self.model(
            login_id=yiban_uid,
            nickname=nickname
        )

        user.set_password("Meiyouluanyong")
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, nickname):
        user = self.create_user(
            login_id,
            nickname=nickname
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    class Meta:
        verbose_name = '用户（开发用）'
        verbose_name_plural = '用户(开发用)'

    MALE = "M"
    FEMALE = "F"
    UNKNOWN = 'U'
    SEX_CHOICES = (
        (FEMALE, "女"),
        (MALE, "男"),
        (UNKNOWN, "保密")
    )
    yiban_id = models.CharField(max_length=100, unique=True, verbose_name='易班id', null=False)
    nickname = models.CharField(max_length=16, verbose_name='昵称')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=UNKNOWN, verbose_name='性别')
    is_admin = models.BooleanField(default=False, verbose_name='管理员')

    USERNAME_FIELD = 'yiban_id'

    objects = UserManager()

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    def as_dict(self):
        return dict(yiban_id=self.yiban_id, nickname=self.nickname, sex=self.sex)

    @property
    def is_authenticated(self):
        return lambda: True
