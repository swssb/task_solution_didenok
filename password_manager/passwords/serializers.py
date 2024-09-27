from rest_framework import serializers

from .models import Password


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ("password", "service_name")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["password"] = instance.get_decrypted_password()
        return representation
