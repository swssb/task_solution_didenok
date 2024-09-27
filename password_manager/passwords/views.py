from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Password
from .serializers import PasswordSerializer


class PasswordView(GenericAPIView):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    lookup_field = "service_name"

    def get(self, request, service_name=None, *args, **kwargs):
        service_name_query_param = request.query_params.get("service_name", None)

        if service_name_query_param:
            passwords = Password.objects.filter(
                service_name__icontains=service_name_query_param
            )
        elif service_name:
            try:
                passwords = Password.objects.filter(service_name=service_name)
            except Password.DoesNotExist:
                return Response(
                    {"detail": "Password not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"detail": "Service name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not passwords.exists():
            return Response(
                {"detail": "No matching services found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PasswordSerializer(passwords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_name, *args, **kwargs):
        password_data = request.data.get("password")

        if not password_data:
            return Response(
                {"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            password_instance = Password.objects.get(service_name=service_name)
            password_instance.password = password_data
            password_instance.save()
            serializer = self.get_serializer(password_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Password.DoesNotExist:
            password_instance = Password.objects.create(
                service_name=service_name, password=password_data
            )
            serializer = self.get_serializer(password_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
