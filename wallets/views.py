from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Wallet
from .serializers import WalletSerializer
from decimal import Decimal
import json


class WalletCreateView(generics.CreateAPIView):
    """Создание кошелька"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletListView(generics.ListAPIView):
    """Список всех кошельков"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletBalanceView(APIView):
    """Баланс кошелька"""
    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, uuid=pk)
        return Response({'balance': wallet.balance}, status=status.HTTP_200_OK)


class WalletOperationView(APIView):
    """Операции с баланс"""
    def post(self, request, pk):
        # Проверяем валидность JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response(
                {'error': 'Invalid JSON format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что обязательные поля присутствуют в запросе
        operation_type = data.get('operationType')
        amount = data.get('amount')

        if operation_type not in ['DEPOSIT', 'WITHDRAW']:
            return Response(
                {'error': 'Invalid operation type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount is None or not isinstance(amount, (int, float, Decimal)) \
                or amount <= 0:
            return Response(
                {'error': 'Invalid amount'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Получаем кошелек с блокировкой для обновления
            wallet = get_object_or_404(
                Wallet.objects.select_for_update(),
                uuid=pk
            )

            # Выполним операцию
            if operation_type == 'DEPOSIT':
                wallet.balance += Decimal(amount)
                wallet.save()
                return Response(
                    {'message': 'Deposit successful',
                     'balance': wallet.balance},
                    status=status.HTTP_200_OK
                )

            elif operation_type == 'WITHDRAW':
                if wallet.balance < Decimal(amount):
                    # Проверяем наличие необходимых средств для списания
                    return Response(
                        {'error': 'Insufficient funds'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                wallet.balance -= Decimal(amount)
                wallet.save()
                return Response(
                    {'message': 'Withdrawal successful',
                     'balance': wallet.balance},
                    status=status.HTTP_200_OK
                )
