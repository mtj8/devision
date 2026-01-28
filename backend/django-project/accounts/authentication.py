from rest_framework.authentication import TokenAuthentication


class CookieTokenAuthentication(TokenAuthentication):
    """
    Token auth that also checks the `auth_token` cookie.
    Falls back to the default header-based token lookup first.
    """

    def authenticate(self, request):
        # Try standard header lookup
        header_auth = super().authenticate(request)
        if header_auth:
            return header_auth

        token = request.COOKIES.get("auth_token")
        if not token:
            return None

        return self.authenticate_credentials(token)

