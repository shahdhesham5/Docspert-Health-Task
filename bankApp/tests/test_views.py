# bankApp/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from bankApp.models import Account, Transactions

class TransactionTests(TestCase):

    def setUp(self):
        # Create two sample accounts for the test
        self.account1 = Account.objects.create(Identifier="12345", name="Account 1", balance=500.0)
        self.account2 = Account.objects.create(Identifier="67890", name="Account 2", balance=300.0)

    def test_valid_transaction(self):
        # Valid transaction between account1 and account2
        response = self.client.post(reverse('transaction'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': 100.0
        })

        # Refresh account instances after the transaction
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()

        # Check that the balances have been updated
        self.assertEqual(self.account1.balance, 400.0)
        self.assertEqual(self.account2.balance, 400.0)

        # Check that the transaction was created
        transaction = Transactions.objects.last()
        self.assertEqual(transaction.from_account, self.account1)
        self.assertEqual(transaction.to_account, self.account2)
        self.assertEqual(transaction.amount, 100.0)

        # Check that a success message is shown
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Transaction completed successfully!')

    def test_insufficient_funds(self):
        # Trying to transfer more money than available in account1
        response = self.client.post(reverse('transaction'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': 600.0
        })

        # Check the balances haven't changed
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 500.0)
        self.assertEqual(self.account2.balance, 300.0)

        # Check that the warning message is shown
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Insufficient funds in the source account.')

    def test_invalid_amount(self):
        # Trying to transfer a negative amount
        response = self.client.post(reverse('transaction'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': -50.0
        })

        # Check that no transaction is made
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account1.balance, 500.0)
        self.assertEqual(self.account2.balance, 300.0)

        # Check the message for invalid amount
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Transaction amount must be greater than zero.')

    def test_same_account(self):
        # Trying to transfer between the same account
        response = self.client.post(reverse('transaction'), {
            'from_account': self.account1.id,
            'to_account': self.account1.id,
            'amount': 100.0
        })

        # Check that no transaction occurs
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 500.0)

        # Check the warning message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Transaction cannot be made between the same account.')

    def test_account_does_not_exist(self):
        # Creating an invalid account ID (non-existent account)
        response = self.client.post(reverse('transaction'), {
            'from_account': 99999,  # Invalid account ID
            'to_account': self.account2.id,
            'amount': 100.0
        })

        # Check that no transaction happens
        self.account2.refresh_from_db()
        self.assertEqual(self.account2.balance, 300.0)

        # Check the error message for account not found
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'One or both of the accounts do not exist.')

    def test_transaction_creation(self):
        # Performing a valid transaction
        self.client.post(reverse('transaction'), {
            'from_account': self.account1.id,
            'to_account': self.account2.id,
            'amount': 100.0
        })

        # Check that a transaction record is created
        transaction = Transactions.objects.last()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.from_account, self.account1)
        self.assertEqual(transaction.to_account, self.account2)
        self.assertEqual(transaction.amount, 100.0)
