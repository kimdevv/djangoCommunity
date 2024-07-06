from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserDetailSerializer
from .models import CustomUser
from board.models import Board
from board.serializers import ViewPostSerializer

# Create your views here.
class Login(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = CustomUser.objects.get(username=username)

        if user is None:
            return Response({
                "message": "존재하지 않는 아이디입니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # CustomUser을 상속받아서 만들면 check_password() 함수가 제공된다
        if not user.check_password(password):
            return Response({
                "message": "비밀번호가 틀렸습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user) # JWT 리프레시 토큰을 발급해주는 시리얼라이저 이용
            refresh_token = str(token)
            access_token = str(token.access_token)

            response = Response({
                "access": access_token,
                "refresh": refresh_token,
                "user": CustomUserDetailSerializer(user).data
            }, status=status.HTTP_200_OK)

            return response
        else:
            return Response({
                "message": "로그인에 실패하였습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
class Info(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user # simplejwt가 jwt에서 user 정보는 바로 추출해 주는 듯...?
        return Response({ # 이렇게 하거나 아니면 시리얼라이저로 보내도 된다 (시리어라이저 만들기 귀찮음 이슈)
            "id": user.id,
            "nickname": user.nickname,
            "university": user.university
        }, status=status.HTTP_200_OK)
    
class Post(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        boards = Board.objects.filter(user=user.id) # 해당 user의 userId를 가진 게시글만 뽑음

        serializer = ViewPostSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)