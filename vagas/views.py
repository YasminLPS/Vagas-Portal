from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import UserRegistrationForm, EmpresaForm, VagaForm, CandidatoForm
from .models import Vaga, Candidato, Empresa 



def registrar(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        empresa_form = EmpresaForm(request.POST)
        
        if user_form.is_valid() and empresa_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password']) 
            user.save()

            empresa = empresa_form.save(commit=False)
            empresa.usuario = user  
            empresa.save()

            return redirect('login') 
    else:
        user_form = UserRegistrationForm()
        empresa_form = EmpresaForm()
        
    return render(request, 'registrar.html', {'user_form': user_form, 'empresa_form': empresa_form})


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