from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import RegisterMedico, RegisterPacientes, RegisterAgenda, RegisterFinanca
from django.urls import reverse_lazy
from django.http import JsonResponse
from django import forms
from .utils import calcular_total_mensalidade, calcular_total_salarios
from datetime import datetime

# Create your views here.

class HomeView(TemplateView):
    template_name = "registrations/home.html"

class RegisterMedicoDeleteView(DeleteView):
    model = RegisterMedico
    template_name = 'registrations/registermedico_confirm_delete.html'
    success_url = reverse_lazy("list_med")

class RegisterPacientesDeleteView(DeleteView):
    model = RegisterPacientes
    template_name ="registrations/registerpacientes_confirm_delete.html"
    success_url = reverse_lazy("list_pac")

class RegisterConsultaDeleteView(DeleteView):
    model = RegisterAgenda
    template_name = 'registrations/registerconsulta_confirm_delete.html'
    success_url = reverse_lazy("list_cons")


def register(request):
    registrations = RegisterMedico.objects.all()
    return render(request, "registrations/medCadsList.html",{"registrations": registrations})

def registerP(request):
    registrations = RegisterPacientes.objects.all()
    return render(request, "registrations/pacCadsList.html", {"registrations": registrations})

def registerC(request):
    registrations = RegisterAgenda.objects.all()
    return render(request,"registrations/consCadsList.html", {"registrations": registrations})

def registerF(request):
    total_salarios = calcular_total_salarios()
    total_receita = calcular_total_mensalidade()
    data_atual = datetime.now().date()
    mes_atual = datetime.now().strftime('%Y-%m')  
    registros_existentes = RegisterFinanca.objects.filter(mesP__year=data_atual.year, mesP__month=data_atual.month)
    
    if registros_existentes.exists():
        
        registro_existente = registros_existentes.first()
        registro_existente.despezas = total_salarios
        registro_existente.receita = total_receita
        registro_existente.save()
    else:
        novo_registro = RegisterFinanca(
            receita=0.00,  
            despezas=total_salarios,
            mesP=data_atual,  
            obs='Total de salários calculado automaticamente'
        )
        novo_registro.save()

    
    registrations = RegisterFinanca.objects.all()
    
    return render(request, "registrations/finanCadsList.html", {"registrations": registrations})





class RegisterMedicoCreateView(CreateView):
    model = RegisterMedico
    fields = ["medicoName", "medicoDateNasc", "medicoCPF", "medicoCEP", "medicoTel", "medicoEmail", "salario", "password"]
    success_url = reverse_lazy('list_med')  

    def form_valid(self, form):
        
        form.instance.is_active = False
        return super().form_valid(form)
    
class RegisterMedicoUpdateView(UpdateView):
    model = RegisterMedico
    fields = ["medicoName", "medicoDateNasc", "medicoCPF", "medicoCEP", "medicoTel", "medicoEmail", "salario", "password"]
    success_url = reverse_lazy('list_med')  

    def form_valid(self, form):
        
        form.instance.is_active = False
        return super().form_valid(form)
    
class RegisterPacientesCreateView(CreateView):
    model = RegisterPacientes
    fields = ["pacienteName", "pacienteDateNasc", "pacienteCPF", "pacienteCEP", "pacienteTel", "pacienteEmail", "password", "mensalidade"]
    success_url = reverse_lazy('list_pac')  
    template_name = "registrations/registerpaciente_form.html"

    def form_valid(self, form):
        
        form.instance.is_active = False
        return super().form_valid(form)
    
class RegisterPacientesUpdateView(UpdateView):
    model = RegisterPacientes
    fields = ["pacienteName", "pacienteDateNasc", "pacienteCPF", "pacienteCEP", "pacienteTel", "pacienteEmail", "password", "mensalidade"]
    success_url = reverse_lazy('list_pac')  
    template_name = "registrations/registerpaciente_form.html"

    def form_valid(self, form):
        
        form.instance.is_active = False
        return super().form_valid(form)


class ConsultaCreateView(CreateView):
    model = RegisterAgenda
    fields = ['nome_medico', 'cpf_paciente', 'data_hora']
    template_name = 'registrations/registerconsulta_form.html'
    success_url = reverse_lazy('list_cons')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Filtra os médicos para mostrar apenas os disponíveis
        form.fields['nome_medico'].queryset = RegisterMedico.objects.all()
        
        # Modifica o campo CPF para um Select, listando todos os CPFs dos pacientes
        form.fields['cpf_paciente'] = forms.ModelChoiceField(
            queryset=RegisterPacientes.objects.all(),
            to_field_name='pacienteCPF',
            empty_label="Selecione o CPF"
        )
        
        # O campo 'nome_paciente' não deve ser acessado aqui, pois não faz parte do formulário
        return form

    def form_valid(self, form):
        cpf_paciente = form.cleaned_data['cpf_paciente']
        try:
            paciente = RegisterPacientes.objects.get(pacienteCPF=cpf_paciente)
            form.instance.nome_paciente = paciente
        except RegisterPacientes.DoesNotExist:
            form.instance.nome_paciente = None
        return super().form_valid(form)
    
class ConsultaUpdateView(UpdateView):
    model = RegisterAgenda
    fields = ['nome_medico', 'cpf_paciente', 'data_hora']
    template_name = 'registrations/registerconsulta_form.html'
    success_url = reverse_lazy('list_cons')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Filtra os médicos para mostrar apenas os disponíveis
        form.fields['nome_medico'].queryset = RegisterMedico.objects.all()
        
        # Modifica o campo CPF para um Select, listando todos os CPFs dos pacientes
        form.fields['cpf_paciente'] = forms.ModelChoiceField(
            queryset=RegisterPacientes.objects.all(),
            to_field_name='pacienteCPF',
            empty_label="Selecione o CPF"
        )
        
        # O campo 'nome_paciente' não deve ser acessado aqui, pois não faz parte do formulário
        return form

    def form_valid(self, form):
        cpf_paciente = form.cleaned_data['cpf_paciente']
        try:
            paciente = RegisterPacientes.objects.get(pacienteCPF=cpf_paciente)
            form.instance.nome_paciente = paciente
        except RegisterPacientes.DoesNotExist:
            form.instance.nome_paciente = None
        return super().form_valid(form)
    
