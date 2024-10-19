from django.db import models
import uuid


class Wallet(models.Model):
    """Модель кошелька"""
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
