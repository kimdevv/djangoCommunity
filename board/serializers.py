from rest_framework import serializers
from django.utils import timezone
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# 게시글 목록만 출력할 거면 이걸로
class ViewPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'created_at', 'comments']

# 이걸 쓰면 게시글의 body도 보여줌
class ViewDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']

class MakePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)

    class Meta:
        model = Board
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at']

    # create 함수를 오버라이딩(?)해서 해당 인스턴스 만들 수 있음
    def create(self, validated_data):
        user = self.context['user_id']
        nickname = self.context['nickname']

        board = Board.objects.create(
            user = user,
            nickname = nickname,
            title = validated_data['title'],
            body = validated_data['body']
        )
        return board
    
    # update 함수가 현재 인스턴스를 수정하는 함수임
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
    
class ViewCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['comments']

class MakeCommentSerializer(serializers.Serializer): # ModelSerializer 말고 Serializer 하면 Meta 없어도 된다
    comment = serializers.CharField()

    def create(self, validated_data):
        post_id = self.context['post_id']
        user_id = self.context['user_id']
        nickname = self.context['nickname']

        board = Board.objects.get(pk=post_id)
        Comment.objects.create(board=board, user=user_id, nickname=nickname, **validated_data)
        return board