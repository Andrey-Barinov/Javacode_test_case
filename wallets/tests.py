from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from rest_framework import status
from .models import Wallet
import uuid


class WalletAPITests(APITestCase):
    def setUp(self):
        self.new_wallet1 = Wallet.objects.create(balance=2000)

    def test_wallet_create_with_right_value(self):
        url = reverse_lazy('wallets:create')
        response = self.client.post(url, {'balance': 1000}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_wallet2 = Wallet.objects.get(balance=1000)

        self.assertTrue(new_wallet2)

    def test_wallet_create_with_wrong_value(self):
        url = reverse_lazy('wallets:create')
        response = self.client.post(url, {'balance': -100}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallets_list(self):
        url = reverse_lazy('wallets:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_wallet_balance(self):
        url = reverse_lazy(
            'wallets:balance',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 2000)

    def test_non_existent_wallet_balance(self):
        url = reverse_lazy('wallets:balance', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wallet_deposit_operation(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.post(
            url,
            {"operationType": "DEPOSIT", 'amount': 1000},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Deposit successful')
        self.assertEqual(response.data['balance'], 3000)

    def test_wallet_withdraw_operation(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.post(
            url,
            {"operationType": "WITHDRAW", 'amount': 1000},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Withdrawal successful')
        self.assertEqual(response.data['balance'], 1000)

    def wallet_withdraw_operation_in_case_of_insufficient_funds(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.post(
            url,
            {"operationType": "WITHDRAW", 'amount': 10000},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Insufficient funds')

    def test_wallet_operation_with_invalid_JSON(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        invalid_JSON = "{'operationType': 'DEPOSIT', 'amount: 100}"
        response = self.client.post(
            url,
            data=invalid_JSON,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid JSON format')

    def test_wallet_operation_with_wrong_operation_type(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.post(
            url,
            {"operationType": "WRONG OPERATION!", 'amount': 1000},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid operation type')

    def test_wallet_operation_with_invalid_amount(self):
        url = reverse_lazy(
            'wallets:operation',
            kwargs={'pk': self.new_wallet1.uuid}
        )
        response = self.client.post(
            url,
            {"operationType": "DEPOSIT", 'amount': 'wrong!'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid amount')
