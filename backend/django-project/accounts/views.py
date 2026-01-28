
# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import User
from .serializers import CustomUserSerializer


from django.shortcuts import render


from .models import User
from .serializers import CustomUserSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request):
        serializer = CustomUserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(CustomUserSerializer(user, context={"request": request}).data)
        return Response(serializer.errors, status=400)

