from django.shortcuts import render,redirect, get_object_or_404
from .models import Account, Transactions
from django.contrib import messages
import csv,io
from django.db import transaction

def upload(request):
    if request.method == 'POST':  # Check if the request method is POST
        new_file = request.FILES['myfile']  # Try to upload file using POST method

        # Check if the file format is supported (CSV, TSV, or XLSX)
        if not new_file.name.endswith(('csv', 'tsv', 'xlsx')):
            messages.warning(request, 'Please upload a valid CSV, TSV, or XLSX file.')
            return redirect('home')

        dataset = new_file.read().decode('UTF-8')  # Decode the file content
        io_string = io.StringIO(dataset)  # Create an io.StringIO object to work with CSV data
        
        # Handle CSV format and TSV (use tab as delimiter for TSV)
        delimiter = ',' if new_file.name.endswith('csv') else '\t'
        
        try:
            next(io_string)  # Skip the first row assuming it's the header
        except StopIteration:
            messages.warning(request, 'Uploaded file is empty.')
            return redirect('home')

        for column in csv.reader(io_string, delimiter=delimiter, quotechar="|"):
            try:
                # Replace Arabic comma (،) with a dot (.) and convert balance to float
                balance = column[2].replace('،', '.')
                balance = float(balance)  # Convert balance to float

                # Handle possible duplicate accounts and account creation
                account, created = Account.objects.update_or_create(
                    Identifier=column[0],
                    defaults={'name': column[1], 'balance': balance},
                )

            except ValueError:
                messages.error(request, "Invalid row")
                continue  # Skip rows with invalid data

        messages.success(request, 'File uploaded successfully!')
        return redirect('home')
    
    return render(request, 'home.html')


def accounts(request):
    accounts = Account.objects.all()
    return render(request,'accounts.html',{'accounts':accounts})


def account_detail(request, id):
    # Fetch the account using the provided ID
    account = get_object_or_404(Account, id=id)

    # Fetch all transactions related to the account
    transactions = Transactions.objects.filter(
        from_account=account
    ) | Transactions.objects.filter(to_account=account)

    return render(request, 'account_detail.html', {
        'account': account,
        'transactions': transactions
    })



def addtransaction(request):
    accounts = Account.objects.all().order_by('created_at')
    if request.method == 'POST':
        from_account_id = request.POST['from_account']  # Getting the id of the selected account
        to_account_id = request.POST['to_account']  # Getting the id of the selected account
        amount = float(request.POST['amount'])

        # Check for a valid amount
        if amount <= 0:
            messages.warning(request, 'Transaction amount must be greater than zero.')
            return redirect('transaction')

        # Ensure source and destination accounts are not the same
        if from_account_id == to_account_id:
            messages.warning(request, 'Transaction cannot be made between the same account.')
            return redirect('transaction')

        try:
            with transaction.atomic():
                # Lock the accounts involved in the transaction
                from_account = Account.objects.select_for_update().get(id=from_account_id)
                to_account = Account.objects.select_for_update().get(id=to_account_id)

                # Check for sufficient funds
                if from_account.balance >= amount:
                # Start a transaction to ensure atomicity
                    # Make the transfer
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    
                    # Record the transaction
                    Transactions.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=amount
                    )
                    messages.success(request, 'Transaction completed successfully!')
                else:
                    messages.warning(request, 'Insufficient funds in the source account.')
        except Account.DoesNotExist:
            messages.warning(request, 'One or both of the accounts do not exist.')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('transactions_history')
    
    return render(request, 'transaction.html', {'accounts': accounts})



def transaction_history(request):
    transactions = Transactions.objects.all().order_by('-date')
    return render(request, 'transactions_history.html', {'transactions': transactions})
