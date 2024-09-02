"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from registrations.views import register, registerP, registerC, registerF, HomeView, RegisterMedicoCreateView, RegisterPacientesCreateView, ConsultaCreateView, RegisterMedicoUpdateView, RegisterPacientesUpdateView, ConsultaUpdateView, RegisterMedicoDeleteView, RegisterPacientesDeleteView, RegisterConsultaDeleteView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",HomeView.as_view(),name="home"),
    path("listM/",register, name="list_med"),
    path("listP/", registerP, name="list_pac"),
    path("listC/", registerC, name="list_cons"),
    path("listF/", registerF, name="list_finan"),
    path("register/", RegisterMedicoCreateView.as_view(), name='register_medico'),
    path("updateM/<int:pk>", RegisterMedicoUpdateView.as_view(), name="update_medico"),
    path("deleteM/<int:pk>", RegisterMedicoDeleteView.as_view(), name="delete_medico"),
    path("registerP/", RegisterPacientesCreateView.as_view(), name="register_paciente"),
    path("updateP/<int:pk>", RegisterPacientesUpdateView.as_view(), name="updade_paciente"),
    path("deleteP/<int:pk>",RegisterPacientesDeleteView.as_view(),name="delete_paciente"),
    path("registerC/", ConsultaCreateView.as_view(), name="register_consulta"),
    path("updateC/<int:pk>", ConsultaUpdateView.as_view(), name="update_consulta"),
    path("deleteC/<int:pk>", RegisterConsultaDeleteView.as_view(), name="delete_consulta"),

   
    

]

