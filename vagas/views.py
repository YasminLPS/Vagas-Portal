from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.db.models import Count

from .forms import UsuarioForm, EmpresaForm, VagaForm, CandidatoForm
from .models import Vaga, Candidato, Empresa 


def registrar(request):
    if request.method == "POST":
        usuario_form = UsuarioForm(request.POST)
        empresa_form = EmpresaForm(request.POST)
        if usuario_form.is_valid() and empresa_form.is_valid():
            # Criar o usuário
            usuario = usuario_form.save()
            # Criar a empresa associando-a ao usuário
            empresa = empresa_form.save(commit=False)
            empresa.usuario = usuario  # Relaciona a empresa ao usuário recém-criado
            empresa.save()
            # Fazer o login do usuário
            login(request, usuario)
            return redirect('vagas_lista')
    else:
        usuario_form = UsuarioForm()
        empresa_form = EmpresaForm()

    return render(request, 'registrar.html', {
        'usuario_form': usuario_form,
        'empresa_form': empresa_form
    })


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vagas_lista')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def vagas_lista(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas_lista.html', {'vagas': vagas})

@login_required
def criar_vaga(request):
    if request.method == "POST":
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = Empresa.objects.get(email=request.user.email) 
            vaga.save()
            return redirect('vagas_lista')
    else:
        form = VagaForm()
    return render(request, 'criar_vaga.html', {'form': form})

@login_required
def aplicar_para_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)  
    if request.method == "POST":
        form = CandidatoForm(request.POST)
        if form.is_valid():
            candidato = form.save(commit=False)
            candidato.vaga = vaga
            candidato.save()
            return redirect('vagas_lista')
    else:
        form = CandidatoForm()
    return render(request, 'aplicar_para_vaga.html', {'form': form, 'vaga': vaga})

def report_data(request):
    vagas_por_mes = Vaga.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id'))
    candidatos_por_mes = Candidato.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id'))

    return JsonResponse({
        'vagas': list(vagas_por_mes),
        'candidatos': list(candidatos_por_mes),
    }, encoder=DjangoJSONEncoder)
    

@login_required
def visualizar_report(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)

    if vaga.empresa.usuario != request.user:
        return render(request, 'acesso_negado.html')  
    candidatos = Candidato.objects.filter(vaga=vaga)
    
    total_candidatos = candidatos.count()

    context = {
        'vaga': vaga,
        'candidatos': candidatos,
        'total_candidatos': total_candidatos
    }
    return render(request, 'visualizar_report.html', context)