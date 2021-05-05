from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_avatar_path(instance, filename):
    #profileの写真の拡張子をextに格納
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])


def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')
        #emailが大文字で入力された場合に小文字に変換するなどの正規化
        user = self.model(email=self.normalize_email(email))
        #passwordをハッシュ化し設定
        user.set_password(password)
        #dbに登録
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    #email用のfield設定。かぶりなしにしたいため、unique=True
    email = models.EmailField(max_length=50, unique=True)
    #アカウントを使用できるようにactiveはTrue
    is_active = models.BooleanField(default=True)
    #adminには入れないようにしたいので、staffはFalse
    is_staff = models.BooleanField(default=False)
    #userクラスからUserManager内のメソッドを使用できるように
    objects = UserManager()

    USERNAME_FIELD = 'email'
    #print等した際にemailを表示
    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    #UserモデルとProfileをonetooneで紐付ける
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    #profileインスタンスが作成された日時を自動的にcreated_onに格納
    created_on = models.DateTimeField(auto_now_add=True)
    #profileの画像用のfield
    #登録したしたくない人もいるためblankとnullをTrue
    #画像を保存する場所をupload_toに設定
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


class Post(models.Model):
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked',blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text