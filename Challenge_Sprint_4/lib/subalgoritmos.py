import os

def linha(tam) -> str:
    return '=' * tam

def cabecalho(txt) -> None:
    print("")
    print(linha(50))
    print(txt.center(50))
    print(linha(50))

def menu(titulo, execucoes) -> None:
    cabecalho(titulo)
    c = 1
    for i in execucoes:
        print(f'{c} - {i}')
        c += 1
    print(linha(50))

# Tratamento de erro para variáveis numéricas
def tratar_erro_num(msg) -> float:
    n = 0
    while True:
        try:
            n = float(input(msg))
            break
        except ValueError:
            print("\033[031m--> ERRO: Por favor, digite um número.\033[m\n")
            continue
    return n

def exibir_invalido() -> None:
    print("\033[031m--> ERRO: Por favor, digite uma opção válida.\033[m\n")

def cadastro_geral(tipo_cadastro, d: dict) -> dict:
    cabecalho(f'CADASTRO {tipo_cadastro}')
    for k in d.keys():
        d[k] = validacoes(k)
    return d

# Permite confirmar/alterar dados já digitados pelo usuário
def confirmar_dados(tipo_cadastro, d: dict) -> dict:
    alterar = "N"
    os.system('cls')
    cont = 0
    opc_alterar = 0
    valores = []
    cabecalho(f'CADASTRO {tipo_cadastro}')
    for k, v in d.items():
        if k.find('Valor') != -1 or k.find('Preço') != -1:
            print(f"{k}: R$ {v:.2f}")
            valores.append(f"{k}: R$ {v:.2f}")
        else:
            print(f"{k}: {v}")
            valores.append(f"{k}: {v}")
    print(linha(50))
    while True:
        alterar = input("Suas informações estão corretas? Digite 'S' para sim ou 'N' para não: ")
        if alterar.upper() == 'S' or alterar.upper() == 'N':
            break
        else:
            exibir_invalido()
    if alterar.upper() == "N":
        menu("ALTERAR DADOS", valores)
        while True:
            opc_alterar = int(tratar_erro_num("Digite a opção que deseja alterar: "))
            if tipo_cadastro == 'DADOS PESSOAIS':
                if opc_alterar in [1, 2, 3, 4, 5]:
                    break
                else:
                    exibir_invalido()
            elif tipo_cadastro == 'DADOS BIKE' or tipo_cadastro.find('Acessório') != -1:
                if opc_alterar in [1, 2, 3, 4]:
                    break
                else:
                    exibir_invalido()
            else:
                if opc_alterar in [1, 2, 3, 4, 5, 6]:
                    break
                else:
                    exibir_invalido()
        for k in d.keys():
            cont += 1
            if opc_alterar == cont:
                if k == 'CEP':
                    nv_dado = ''
                    print("\033[031m--> Infelizmente, não é possível alterar o CEP.\033[m\n")
                    input('Pressione ENTER para continuar')
                else:
                    d[k] = validacoes(k)
                    nv_dado = d[k]
    if alterar.upper() == "S":
        os.system("cls")
        nv_dado = ''
    return d, alterar.upper(), opc_alterar, nv_dado

def exibir_dados(tipo_cadastro, d: dict) -> None:
    cabecalho(tipo_cadastro)
    for k, v in d.items():
        if k.find('Valor') != -1 or k.find('Preço') != -1:
            print(f"{k}: R$ {v:.2f}")
        else:
            print(f"{k}: {v}")
    print(linha(50))

def exibir_descricao_plano(plano) -> None:
    if plano == 'Pedal essencial':
        print("""\033[1m--> Pedal Essencial:\033[0m plano gratuito que oferece 
reparo e/ou troca de câmaras de ar, correntes, 
coroas, manetes de freios, além de 
lubrificação de correntes.""")
    elif plano == "Pedal leve":
        print("""\033[1m--> Pedal leve:\033[0m mesmas garantias do plano Pedal 
Essencial(reparo e/ou troca de câmaras de ar, 
correntes, coroas, manetes de freios, além de 
lubrificação de correntes), com um benefício 
a mais: transporte do segurado e sua bike em 
caso de quebra ou acidente, com limite de 
\033[1m50 km\033[0m.""")
    else:
        print("""\033[1m--> Pedal elite:\033[0m mesmas garantias do plano Pedal 
Essencial(reparo e/ou troca de câmaras de ar, 
correntes, coroas, manetes de freios, além de 
lubrificação de correntes), com um benefício 
a mais: transporte do segurado e sua bike em 
caso de quebra ou acidente, com limite de 
\033[1m150 km\033[0m.""")

def validacoes(dado) -> None:
    if dado == 'Valor':
        return validar_valor()
    elif dado == 'Preço do acessório':
        return validar_preco()
    elif dado == 'Complemento(opcional)':
        valor = input(f"{dado}: ")
        return valor
    elif dado == 'Email':
        return validar_email()
    elif dado == 'CPF':
        return validar_cpf()
    elif dado == "Número":
        numero = tratar_erro_num("Número: ")
        return numero
    elif dado == 'Telefone':
        return validar_telefone()
    else:
        while True:
            valor = input(f"{dado}: ")
            if valor == '':
                print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
            else:
                break
        return valor

def validar_valor() -> float:
    valor = 0
    while True:
        try:
            valor = tratar_erro_num("Valor: R$ ")
            if valor > 2000 or valor == 2000:
                break
            else:
                print("\033[031m--> ERRO: O valor mínimo de uma bike para que seja assegurada é de R$2000.00!!\033[m\n")
        except ValueError:
            print("\033[031m--> ERRO: Por favor, digite um número.\033[m\n")
            continue
    return valor
def validar_preco() -> float:
    preco = tratar_erro_num("Preço do acessório: R$ ")
    return preco
def validar_email() -> str:
    caracteres_especiais = ('[!#$%^&*()_+}{=[\-<>?~/|],;:~`')
    validacao = False
    while not validacao:
        email = input("Email: ")
        if email == '':
            print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
        elif email.find('@') == -1:
            print("\033[031m--> ERRO: Seu email não possui um '@'.\033[m\n")
        else:
            validacao = True
            for x in email:
                for y in caracteres_especiais:
                    if x == y:
                        print("\033[031m--> ERRO: Não são permitidos caracteres especiais em um email.\033[m\n")
                        validacao = False
    return email
def validar_cpf():
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while True:
        numeros_cpf = ''
        cpf = input("CPF: ")
        if cpf == '':
            print("\033[031m--> ERRO: Por favor, digite seus dados.\033[m\n")
        else:
            # Remove caracteres não numéricos do CPF
            for char in cpf:
                if char in numeros:
                    numeros_cpf += str(char)

            # Verifica se o CPF tem 11 dígitos
            if len(numeros_cpf) != 11:
                print("\033[031m--> ERRO: CPF não possui a quantidade de dígitos necessária.\033[m\n")
            else:
                # Calcula o primeiro dígito verificador
                total = 0
                for i in range(9):
                    total += int(numeros_cpf[i]) * (10 - i)
                resto = total % 11
                if resto < 2:
                    dv1 = 0
                else:
                    dv1 = 11 - resto

                # Calcula o segundo dígito verificador
                total = 0
                for i in range(10):
                    total += int(numeros_cpf[i]) * (11 - i)
                resto = total % 11
                if resto < 2:
                    dv2 = 0
                else:
                    dv2 = 11 - resto

                # Verifica se os dígitos verificadores calculados coincidem com os dígitos no CPF
                if int(numeros_cpf[9]) == dv1 and int(numeros_cpf[10]) == dv2:
                    break
                else:
                    print("\033[031m--> ERRO: CPF inválido.\033[m\n")
    return cpf
def validar_telefone():
    caracteres_validos = '0123456789 )(-'
    numeros = '0123456789'
    validacao = False
    telefone_numeros = ''
    while not validacao:
        telefone = input("Telefone (XX) XXXXX-XXXX: ")
        validacao = True
        for x in telefone:
            if x not in caracteres_validos:
                validacao = False
                print("\033[031m--> ERRO: Por favor, digite apenas números ou caracteres válidos.\033[m\n")
                break
        for t in telefone:
            for n in numeros:
                if t == n:
                    telefone_numeros += t
        if len(telefone_numeros) < 10:
            validacao = False
            print("\033[031m--> ERRO: Digite um telefone válido.\033[m\n")
    return telefone