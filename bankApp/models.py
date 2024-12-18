from django.db import models

# Create your models here.
class Account (models.Model):
    Identifier = models.CharField(max_length=255,null=True, blank=True)
    name = models.CharField(("name"), max_length=255,null=True, blank=True)
    balance = models.FloatField(("balane"),null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name
    
    
class Transactions(models.Model):
    from_account = models.ForeignKey(Account, related_name='transactions_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='transactions_to', on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction from {self.from_account.name} to {self.to_account.name} of {self.amount}'
