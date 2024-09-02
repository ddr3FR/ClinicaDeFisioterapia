from registrations.models import RegisterPacientes, RegisterMedico
from django.db.models import Sum

def calcular_total_mensalidade():
    total = RegisterPacientes.objects.aggregate(total_mensalidade=Sum('mensalidade'))['total_mensalidade']
    return total if total else 0

def calcular_total_salarios():
    total = RegisterMedico.objects.aggregate(total_salario=Sum('salario'))['total_salario']
    return total if total else 0