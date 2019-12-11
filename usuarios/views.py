from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from django.conf import settings

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # validando senhas
        if password == password2:
            # verificando se o usuário já está cadastrado
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email já cadastradado. Por favor utilize outro email')
                print('email já cadastrado')
                return redirect('cadastro')
            else:
                user = User.objects.create_user(username=nome, email=email, password=password)
                user.save()
                messages.success(request, 'Cadastro realizado com sucesso')
                return redirect('login')
        else:
            messages.error(request, 'As senhas não conferem')
        return redirect('cadastro')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email== "" or senha == "":
            messages.error(request, 'O campos email e senha precisam ser preenchidos')
        else:
            if User.objects.filter(email=email).exists():
                nome = User.objects.filter(email=email).values_list('username',flat=True).get()
                user = auth.authenticate(request, username=nome, password=senha)
                if user is not None:
                    auth.login(request, user)
                    print('login realizado com sucesso')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Email ou senha não estão corretos')
                    redirect('login')
            else:
                messages.error(request, 'Email não encontrado')
                redirect('login')
    return render(request,'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    id = request.user.id
    receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)

    dados = {
        'receitas' : receitas
    }
    return render(request, 'usuarios/dashboard.html', dados)

def form_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        
        return render(request, 'usuarios/form_receita.html')

