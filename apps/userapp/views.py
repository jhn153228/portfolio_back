import status as status
from django.conf import settings
from drf_spectacular.utils import extend_schema

from apps.userapp.models import Users
from apps.userapp.serializers.user_serializers import (
    LoginRequestSerializer,
    UserCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


User = Users


class LoginView(APIView):

    @extend_schema(
        request=LoginRequestSerializer,
    )
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)

        if serializer.is_valid():
            user = Users.objects.filter(
                username=serializer.validated_data["user"]["username"]
            ).first()
            return LoginResponse(user)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginResponse(Response):
    def __init__(self, user: Users):
        super().__init__(status=status.HTTP_200_OK)

        token = RefreshToken.for_user(user)

        refresh = str(token)
        access = str(token.access_token)

        self.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access,
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        self.set_cookie(
            key="refresh_token",
            value=refresh,
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        self.data = {
            "refresh": refresh,
            "access": access,
        }


class SignupView(APIView):
    authentication_classes = []  # 인증 클래스 사용 안 함
    permission_classes = [AllowAny]  # 모든 사용자 접근 가능

    @extend_schema(
        request=UserCreateSerializer,
    )
    # AllowAny: 인증되지 않은 사용자도 접근 가능

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # 블랙리스트에 추가하여 사용 불가능하게 만듦
#             return Response({"detail": "Logout successful"}, status=200)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
