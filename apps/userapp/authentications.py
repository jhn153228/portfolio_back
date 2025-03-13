from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from config import settings

User = get_user_model()

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomJWTAuthenticationExtension(
    OpenApiAuthenticationExtension
):  #  drf-spectacular 문서에서 사용할 수 있도록 확장
    target_class = "apps.userapp.authentications.CustomJWTAuthentication"
    name = "JWT Authentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 부모 클래스에서 JWT 토큰을 가져옴
        raw_token_cookie = (
            request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None
        )
        raw_token_header = request.headers.get("X-Access-Token") or None

        raw_token = raw_token_cookie or raw_token_header
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        # ✅ 여기서 추가 정보를 가져올 수 있음
        try:
            user = self.get_user(validated_token)
        except Exception:
            raise AuthenticationFailed("User not found or invalid token.")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive.")

        return user, validated_token

    def get_user(self, validated_token):
        """
        토큰에서 `user_id` 값을 가져와서 해당 유저를 반환
        """
        user_id = validated_token.get("user_id")

        if not user_id:
            raise InvalidToken("Token contained no user identification")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return user
