from django.shortcuts import render
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.authtoken.models import Token
from budget.models import Budget, Transactions
from .serializers import BudgetSerializer, TransactionsSerializer
from django.db.models import Sum

class LoginView(APIView):
    permission_classes=[]
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user     = authenticate(request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login Successfully',
                    'token': token.key
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            request.user.auth_token.delete()  
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = TransactionsSerializer

    def get_queryset(self):
        return Transactions.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        self._update_budget(transaction, transaction.amount)

    def perform_update(self, serializer):
        pervious_data     = self.get_object()
        old_amount        = pervious_data.amount
        current_data      = serializer.save(user=self.request.user)
        amount_diff       = current_data.amount - old_amount
        if (pervious_data.type != current_data.type or pervious_data.datetime.month != current_data.datetime.month or pervious_data.datetime.year  != current_data.datetime.year):
            self._update_budget(pervious_data, -old_amount)
            self._update_budget(current_data, current_data.amount)
        else:
            self._update_budget(current_data, amount_diff)

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        self._update_budget(transaction, -transaction.amount)
        self.perform_destroy(transaction)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update_budget(self, transaction, amount_delta):
        
        budget, _    = Budget.objects.get_or_create(
            user     = transaction.user,
            month    = transaction.datetime.month,
            year     = transaction.datetime.year,
            defaults = {'income': 0, 'expense': 0}
        )
        if transaction.type == 'income':
            budget.income = max(budget.income + amount_delta, 0)
        else:  
            budget.expense = max(budget.expense + amount_delta, 0)
        budget.save()




class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = BudgetSerializer
    queryset           = Budget.objects.all()



class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            year         = request.GET.get('year')
            month        = request.GET.get('month')
            summary_data = Budget.objects.filter(user=request.user, year=year, month=month).values('income', 'expense').first()
            if not summary_data:
                return Response({'message':"No Data"})
            return Response({
                'income': float(summary_data['income']),
                'expense': float(summary_data['expense'])
            })
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

class AvilableYears(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            years = Budget.objects.filter(user=request.user).values_list('year', flat=True).distinct()
            return Response(list(years))
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MonthFromYear(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            year=request.GET.get("year")
            month = Budget.objects.filter(user=request.user,year=year).values_list('month', flat=True).distinct()
            return Response(list(month))
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    