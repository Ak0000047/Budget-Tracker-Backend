from rest_framework import serializers
from .models import Transactions,Budget


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'amount', 'datetime', 'category_name', 'type']
        read_only_fields = ['datetime']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'month', 'year','income','expense']
