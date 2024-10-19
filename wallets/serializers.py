from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор кошелька"""
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'uuid',
            'balance',
        )

    def validate_balance(self, value):
        """Проверка на ввод правильного числа при создании кошелька"""
        if value < 0:
            raise serializers.ValidationError(
                "Balance must be a non-negative number."
            )

        return value
