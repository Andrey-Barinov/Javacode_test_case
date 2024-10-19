from django.urls import path
from .views import (
    WalletCreateView,
    WalletBalanceView,
    WalletListView,
    WalletOperationView
)

app_name = 'wallets'


urlpatterns = [
    path('', WalletCreateView.as_view(), name='create'),
    path('<uuid:pk>/', WalletBalanceView.as_view(), name='balance'),
    path('<uuid:pk>/operation/',
         WalletOperationView.as_view(),
         name='operation'
         ),
    path('list/', WalletListView.as_view(), name='list'),
]
