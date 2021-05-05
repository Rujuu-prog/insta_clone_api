from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    #オプションを記載
    class Meta:
        #現在アクティブなUserモデルをmodelに格納
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True}}
    
    #validateを通ったid、email、passwordが辞書型でvalidated_dataに入る
    def create(self, validated_data):
        #userを作成
        #get_user_model()は現在アクティブなUserモデルを取得
        #modelsのUserのobjectからUserManagerのcreate_userを呼び出す
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    #作成した時間の表示形式を変更
    #日時はクライアント側から指定することはないためreadonly
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model=Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        #userProfileは自動で作成されるようにするため、readonlyに
        extra_kwargs = {'userProfile': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img','liked')
        #userPostは投稿したuserなので、自動で設定するためreadonly
        extra_kwargs = {'userPost': {'read_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','post')
        #上記userPostと同様
        extra_kwargs = {'userComment': {'read_only': True}}