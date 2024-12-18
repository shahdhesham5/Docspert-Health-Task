from django.urls import path
from . import views

urlpatterns = [
path('', views.upload, name='home'),
path('accounts', views.accounts, name='accounts'),
path('account/<int:id>/', views.account_detail, name='account_detail'),
path('transaction', views.addtransaction, name='transaction'),
path('transactions-history', views.transaction_history, name='transactions_history'),
]