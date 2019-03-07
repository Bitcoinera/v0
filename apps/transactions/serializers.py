from rest_framework import serializers

from apps.transactions.models import Transaction


class TransactionToJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('key', 'value', 'created')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Transaction
        fields = ('key', 'value')
        extra_kwargs = {
            'url': {
                'view_name': 'transactions:transaction-detail',
            }
        }
