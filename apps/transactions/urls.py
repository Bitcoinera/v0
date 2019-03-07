from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.transactions import views
app_name = 'transactions'

urlpatterns = [
    url(r'^transactions/$', views.TransactionList.as_view(), name='transaction-list'),
    url(r'^transaction/(?P<pk>[0-9]+)/$', views.TransactionDetail.as_view(), name='transaction-detail'),
    url(r'^transactions-overview/$', views.TransactionFormView.as_view(), name='transactions-overview'),
    url(r'^show-linked-transactions/(?P<pk>[0-9a-zA-Z]+)/$', views.LinkedTransactionsView.as_view(),
        name='show-linked-transactions'),
    url(r'^submit-transactions-to-ethereum/$', views.SubmitTransactionToEthereumView.as_view(),
        name='submit-transactions-to-ethereum'),

]