from apps.transactions.models import Transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from apps.transactions.serializers import TransactionSerializer
from apps.transactions.forms import TransactionForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from rest_framework.reverse import reverse
from django.urls import reverse as django_reverse
from rest_framework.views import APIView
from web3 import Web3
from web3 import HTTPProvider
import os
from rest_framework.status import HTTP_200_OK
from django.conf import settings
from apps.transactions.serializers import TransactionToJsonSerializer
from rest_framework.renderers import JSONRenderer
import hashlib

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
       #'users': reverse('users:user-list', request=request, format=format),
       'transactions': reverse('transactions:transaction-list', request=request, format=format),
       'track_transactions': request.build_absolute_uri(django_reverse(('transactions:transactions-overview')))
})


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save()


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().filter(user=self.request.user)


class TransactionFormView(FormView):
    template_name = 'transaction_form.html'
    form_class = TransactionForm
    selected_transaction = None

    def get_success_url(self):

        return reverse('transactions:show-linked-transactions',
                       kwargs={'pk': self.selected_transaction.id})

    def form_valid(self, form):
        self.selected_transaction = form.cleaned_data['transaction']
        return super().form_valid(form)


class LinkedTransactionsView(TemplateView):
    template_name = 'linked_transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_pk = kwargs['pk']
        selected_transaction = Transaction.objects.get(id=transaction_pk)
        linked_transactions = Transaction.objects.filter(key=selected_transaction.key)
        context['transaction_value'] = selected_transaction.value
        context['linked_transactions'] = linked_transactions

        return context


class SubmitTransactionToEthereumView(TemplateView):
    template_name = 'submission_results.html'

    def get_eth_provider(self, provider_name):
        # open a connection to a local ethereum node (ganache geth or simple in memory blockchain)
        if provider_name == "in_memory_test_rpc":
            return Web3.TestRPCProvider()

        eth_providers = {
            'local': HTTPProvider('http://localhost:9545'),
            'rinkeby': Web3.IPCProvider(settings.RINKEBY_SOCKET_FILE_PATH),
        }

        return eth_providers[provider_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_transactions = TransactionToJsonSerializer(Transaction.objects.all(), many=True)

        all_transactions_json = JSONRenderer().render(all_transactions.data)
        hash_function = hashlib.sha3_512()
        hash_function.update(all_transactions_json)

        hash_of_database = hash_function.hexdigest()
        print('successfully hashed database: {}'.format(hash_of_database))

        # web3.py instance
        provider_to_use = self.get_eth_provider(settings.NETWORK_TO_USE)
        w3 = Web3(provider_to_use)
        if settings.NETWORK_TO_USE == 'rinkeby':
            # this is necessary because of the special consensus mechanism of rinkeby:
            # https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
            from web3.middleware import geth_poa_middleware
            # inject the poa compatibility middleware to the innermost layer
            w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        # set pre-funded account as sender
        w3.eth.defaultAccount = w3.eth.accounts[settings.ETHER_WALLET_ID_TO_USE]

        txn_hash = w3.eth.sendTransaction({
            'from': w3.eth.accounts[settings.ETHER_WALLET_ID_TO_USE],
            'to': w3.eth.accounts[settings.ETHER_WALLET_ID_TO_USE],
            'data': hash_of_database.encode('utf-8'),
            'value': 0,
        })
        print('submitting transaction hash to ethereum: {}'.format(txn_hash))
        print('waiting for transaction receipt......')
        tx_hash_decoded = txn_hash.hex()
        #tx_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
        #print('received transaction receipt: {}'.format(tx_receipt))

        #submitted_transaction = w3.eth.getTransaction(txn_hash)
        new_transaction = Transaction(
            key=hash_of_database,
            value=tx_hash_decoded
        )
        new_transaction.save()
        context['submitted_hash'] = hash_of_database
        context['transaction_id'] = tx_hash_decoded
        print('Submitted Transaction')

        return context


