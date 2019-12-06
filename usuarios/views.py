from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
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
            if User.objects.filter(username=nome).exists():
                print('Email já cadastrado')
                return redirect('cadastro')
            else:
                user = User.objects.create_user(username=nome, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            print('Senhas diferentes')
        return redirect('cadastro')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        senha = request.POST['senha']
        user = auth.authenticate(request, username=nome, password=senha)
        v = user is not None
        print(v)
        if user is not None:
            auth.login(request, user)
            print('login realizado com sucesso')
            return redirect('dashboard')
        else:
            print('\nAlgo errado não estava certo!\n')
            redirect('login')
    return render(request,'usuarios/login.html')


def logout(request):
    auth.logout(request)
    print('Logout realizado com sucesso')
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
        user = get_object_or_404(User, pk=request.user.id)
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria, foto_receita=foto_receita)
        receita.save()
        print('Receita salva com sucesso, graças a Deus')
        return redirect('dashboard')
    else:
        print('algo deu ruim')
        return render(request, 'usuarios/form_receita.html')

