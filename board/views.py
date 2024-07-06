from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from .models import Board
from member.models import CustomUser

# Create your views here.
class PostAPIs(APIView):
    authentication_classes = [JWTAuthentication]

    @method_decorator(permission_classes([AllowAny])) # 이 데코레이터 쓰면 method별로 다 다르게 권한 지정 가능
    def get(self, request):
        posts = Board.objects.all() # 모든 글을 가져옴
        serializer = ViewPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        # user 정보 갖고옴
        user = request.user
        user_id = user.id
        nickname = user.nickname

        # context 옵션을 사용하면 views.py의 데이터를 시리얼라이저로 보낼 수 있음
        serializer = MakePostSerializer(data=request.data, context={'user_id': user_id, 'nickname': nickname})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetailAPIs(APIView):
    authentication_classes = [JWTAuthentication]

    @method_decorator(permission_classes([AllowAny]))
    def get(self, request, post_id):
        board = Board.objects.get(pk=post_id) # 해당 pk에 해당하는 게시글만 가져옴
        serializer = ViewDetailSerializer(board)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @method_decorator(permission_classes([IsAuthenticated]))
    def put(self, request, post_id):
        board = Board.objects.get(pk=post_id) # 해당 pk에 해당하는 게시글들
        serializer = MakePostSerializer(board, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        board = Board.objects.get(pk=post_id)
        board.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentAPIs(APIView):
    authentication_classes = [JWTAuthentication]

    @method_decorator(permission_classes([AllowAny]))
    def get(self, request, post_id):
        board = Board.objects.get(pk=post_id)
        serializer = ViewCommentSerializer(board, data=request.data)

        if serializer.is_valid():
            serializer.save()
            # 응답된 데이터 중 'comments'에 담긴 요소들만 보여준다
            return Response(serializer.data.get('comments'), status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request, post_id):
        user = request.user
        user_id = user.id
        nickname = user.nickname

        board = Board.objects.get(pk=post_id)
        serializer = MakeCommentSerializer(data=request.data, context={'post_id': post_id, 'user_id': user_id, 'nickname': nickname})

        if serializer.is_valid():
            board = serializer.save() # 이 시리얼라이저는 modelSerializer이 아니고 Board 객체를 반환한다
            return Response(ViewPostSerializer(board).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteComment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()

        board = Board.objects.get(pk=post_id)
        serializer = ViewPostSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostByUnivAPIs(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    # Board에 user을 넣은 게 아니라 userId를 넣어버려서 selected_related나 prefatch_related를 못 쓴다ㅜㅜ
    # user을 넣었어야 했는데 제가 멍청했내요
    #https://velog.io/@rosewwross/Django-selectrelated-%EC%99%80-prefetchedrelated%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B0%B8%EC%A1%B0
    def get(self, request, university_name):
        users = CustomUser.objects.filter(university=university_name)
        userIds = users.values_list('id', flat=True) # Thanks to ChatGPT... user의 id 리스트를 불러온다

        boards = Board.objects.filter(user__in=userIds) # Thanks to ChatGPT... __in을 사용하면 해당 리스트 내의 값들을 모두 탐색 가능
        
        serializer = ViewPostSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)