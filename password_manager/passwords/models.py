from cryptography.fernet import Fernet
from django.db import models

key = Fernet.generate_key()
cipher_suite = Fernet(key)


class Password(models.Model):
    password = models.CharField(max_length=255)
    service_name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.password = cipher_suite.encrypt(self.password.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_password(self):
        return cipher_suite.decrypt(self.password.encode()).decode()
