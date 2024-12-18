from django.contrib import admin
from .models import Account, Transactions
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('Identifier', 'name', 'balance', 'created_at')
    ordering = ('created_at',)
    
@admin.register(Transactions)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'to_account', 'amount', 'date')
    ordering = ('date',)
    
  