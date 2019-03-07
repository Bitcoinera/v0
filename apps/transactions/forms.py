from django import forms
from apps.transactions.models import Transaction


class TransactionForm(forms.Form):
    transaction = forms.ModelChoiceField(queryset=Transaction.objects.all())
