from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models import Sum

# Create your models here.


class RegisterMedico(models.Model):
    id_Medico = models.AutoField(primary_key=True)
    medicoName = models.CharField(
        verbose_name="Nome", max_length=100, null=False, blank=False
    )
    medicoDateNasc = models.DateField(
        verbose_name="Data de Nascimento", null=False, blank=False
    )
    medicoCPF = models.CharField(
        verbose_name="CPF", max_length=11, null=False, blank=False
    )
    medicoCEP = models.CharField(
        verbose_name="CEP", max_length=100, null=False, blank=False
    )
    medicoTel = models.CharField(
        verbose_name="Telefone", max_length=11, null=False, blank=False
    )
    medicoEmail = models.EmailField(
        verbose_name="E-mail", max_length=254, null=False, blank=False
    )
    password = models.CharField(max_length=1000, null=False, blank=False)
    salario = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )

    pagMes = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.medicoName}"


class RegisterPacientes(models.Model):
    id_Paciente = models.AutoField(primary_key=True)
    pacienteName = models.CharField(
        verbose_name="Nome", max_length=100, null=False, blank=False
    )
    pacienteDateNasc = models.DateField(
        verbose_name="Data de Nascimento", null=False, blank=False
    )
    pacienteCPF = models.CharField(
        verbose_name="CPF", max_length=11, null=False, blank=False
    )
    pacienteCEP = models.CharField(
        verbose_name="CEP", max_length=100, null=False, blank=False
    )
    pacienteTel = models.CharField(
        verbose_name="Telefone", max_length=11, null=False, blank=False
    )
    pacienteEmail = models.EmailField(
        verbose_name="E-mail", max_length=254, null=False, blank=False
    )
    password = models.CharField(max_length=1000, null=False, blank=False)

    mensalidade = models.DecimalField(
        verbose_name="Mensalidade", max_digits=10, decimal_places=2, null=False, blank=False
    )
    pagMes = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pacienteCPF}"

class RegisterAgenda(models.Model):
    id_Agendamento = models.AutoField(primary_key=True)
    nome_paciente = models.ForeignKey(RegisterPacientes, on_delete=models.CASCADE)
    nome_medico = models.ForeignKey(RegisterMedico, on_delete=models.CASCADE)
    cpf_paciente = models.CharField(max_length=200)
    data_hora = models.DateTimeField(null=False, blank=False)
    

class RegisterFinanca(models.Model):
    receita = models.DecimalField(max_digits=10, decimal_places=2)
    despezas = models.DecimalField(max_digits=10, decimal_places=2)
    mesP = models.DateField()
    obs = models.TextField()

    def calcular_receita(self):
        return RegisterPacientes.objects.aggregate(total_mensalidade=Sum('mensalidade'))['total_mensalidade'] or 0.00

    def save(self, *args, **kwargs):
        self.receita = self.calcular_receita()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"R$: {self.receita} em {self.mesP}"

