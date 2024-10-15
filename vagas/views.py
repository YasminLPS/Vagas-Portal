from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, EmpresaForm

def registrar(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        empresa_form = EmpresaForm(request.POST)
        
        if user_form.is_valid() and empresa_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Definindo a senha corretamente
            user.save()

            empresa = empresa_form.save(commit=False)
            empresa.usuario = user  # Associe a empresa ao usuário
            empresa.save()

            return redirect('login')  # Redireciona após o registro
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
                return redirect('vagas_lista')  # Redireciona para a lista de vagas após o login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})