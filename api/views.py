from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment


#新規ユーザーを作成するためのview
#createのみの機能なので汎用APIView
class CreateUserView(generics.CreateAPIView):
    #新規作成のみの役割なので、querysetでobjectを取得する必要はない
    serializer_class = serializers.UserSerializer
    #JWTの認証を通っていないuserでもアクセスできるように設定
    permission_classes = (AllowAny,)

#新規作成と更新をするためmodelView
class ProfileViewSet(viewsets.ModelViewSet):
    #更新のために全てのobjectを取得
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    #新規で作成する際に呼ばれるメソッド
    #request.userで現在ログインしているユーザーを取得しuserProfileに格納
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)

#loginしているユーザーのプロフィールリストを返してくれるview
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    #loginしているuserと一致しているプロフィールを返す
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)

#投稿に対するview
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)