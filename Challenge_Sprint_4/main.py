from lib.subalgoritmos import *
from lib.conexoes import *
import os
from time import sleep

funcionalidades = ['Ver/Cadastrar dados pessoais', 'Ver/Cadastrar dados da bike', 'Ver/Selecionar plano',
                   'Fechar o programa']
dados = {
    'Dados Pessoais':
        {
            'Nome': "",
            'Email': "",
            'Telefone': "",
            'CPF': "",
            'CEP': ""
        },
    'Dados Bike':
        {
            'Marca': "",
            'Modelo': "",
            'Chassi': "",
            'Valor': 0.0
        },
    'Endereco': {}
}
acessorio = {
    'Tipo do acessório': "",
    'Marca do acessório': "",
    'Modelo do acessório': "",
    'Preço do acessório': 0.0
}
quant_acessorio = 0
opc_plano = 0
escolha_alterar = "N"
plano_selecionado = ""
alterar_plano = ""
d_pessoais_cadastrados = False
d_bike_cadastrados = False
dados_restantes = []
finalizar_programa = ""

os.system('cls')
print(f"""
{linha(61)}
|| Bem-vindo ao programa responsável pela contratação do   ||
|| seguro de bikes via Porto Seguro.                       ||
|| Desenvolvido por: CycleX                                ||
{linha(61)}
""")
sleep(3)
while True:

    # Menu principal de interação
    menu('MENU PRINCIPAL', funcionalidades)
    opc_menu = int(tratar_erro_num("Escolha uma opção: "))
    match opc_menu:

        # Cadastro de dados pessoais
        case 1:
            if not d_pessoais_cadastrados:
                dados['Dados Pessoais'] = cadastro_geral('DADOS PESSOAIS', dados['Dados Pessoais'])
                insert_bd('cliente', dados['Dados Pessoais'])

                dados['Endereco'] = viacep_api(dados['Dados Pessoais']['CEP'])
                insert_bd('endereco', dados['Endereco'])

                while escolha_alterar == 'N':
                    dados['Dados Pessoais'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('DADOS PESSOAIS', dados['Dados Pessoais'])
                    if novo_dado != '':
                        update_bd('cliente', opc_alterar, novo_dado)
                escolha_alterar = 'N'
                while escolha_alterar == 'N':
                    dados['Endereco'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('ENDEREÇO', dados['Endereco'])
                    if novo_dado != '':
                        update_bd('endereco', opc_alterar, novo_dado)
                escolha_alterar = 'N'
                d_pessoais_cadastrados = True
                cabecalho("Cadastro de dados pessoais finalizado!!!")

            # Caso o cliente já tenha digitado seus dados, ele pode alterá-los ao entrar nesta área novamente
            else:
                while escolha_alterar == 'N':
                    dados['Dados Pessoais'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('DADOS PESSOAIS', dados['Dados Pessoais'])
                    if novo_dado != '':
                        update_bd('cliente', opc_alterar, novo_dado)
                escolha_alterar = 'N'
                while escolha_alterar == 'N':
                    dados['Endereco'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('ENDEREÇO', dados['Endereco'])
                    if novo_dado != '':
                        update_bd('cliente', opc_alterar, novo_dado)
                escolha_alterar = 'N'

        # Cadastro de dados da bike
        case 2:
            if not d_bike_cadastrados:
                dados['Dados Bike'] = cadastro_geral('DADOS BIKE', dados['Dados Bike'])
                insert_bd('bike', dados['Dados Bike'])
                
                while escolha_alterar == 'N':
                    dados['Dados Bike'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('DADOS BIKE', dados['Dados Bike'])
                    if novo_dado != '':
                        update_bd('bike', opc_alterar, novo_dado)
                escolha_alterar = 'N'

                # Cadastro dos possíveis acessórios da bike
                while True:
                    possui_acessorio = input("Sua bike possui algum acessório? [S/N]: ")
                    if possui_acessorio.upper() == 'S' or possui_acessorio.upper() == 'N':
                        break
                    else:
                        exibir_invalido()
                if possui_acessorio.upper() == 'S':
                    quant_acessorio = int(tratar_erro_num("Quantos?: "))
                    for i in range(quant_acessorio):
                        dados[f'Acessório {i + 1}'] = acessorio
                        dados[f'Acessório {i + 1}'] = cadastro_geral(f'ACESSÓRIO {i + 1}', dados[f'Acessório {i + 1}'])
                        insert_bd('acessorio', dados[f'Acessório {i + 1}'])
                        while escolha_alterar == 'N':
                            dados[f'Acessório {i + 1}'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados(f'ACESSÓRIO {i + 1}', dados[f'Acessório {i + 1}'])
                            if novo_dado != '':
                                update_bd('acessorio', opc_alterar, novo_dado)
                        escolha_alterar = 'N'
                if possui_acessorio.upper() == 'N':
                    os.system("cls")
                d_bike_cadastrados = True
                cabecalho("Cadastro de dados da bike finalizado!!!")

            # Permite ao cliente alterar estes dados ao entrar novamente
            else:
                while escolha_alterar == 'N':
                    dados['Dados Bike'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados('DADOS BIKE', dados['Dados Bike'])
                    if novo_dado != '':
                        update_bd('bike', opc_alterar, novo_dado)
                escolha_alterar = 'N'
                if quant_acessorio != 0:
                    for i in range(quant_acessorio):
                        while escolha_alterar == 'N':
                            dados[f'Acessório {i + 1}'], escolha_alterar, opc_alterar, novo_dado = confirmar_dados(f'ACESSÓRIO {i + 1}', dados[f'Acessório {i + 1}'])
                            if novo_dado != '':
                                update_bd('acessorio', opc_alterar, novo_dado)
                        escolha_alterar = 'N'

        # Selecionar plano da bike
        case 3:
            while True:
                if opc_plano != 4:
                    os.system('cls')
                if plano_selecionado == "":
                    cabecalho("SELECIONE SEU PLANO")
                    print(f"""1 --> Pedal essencial: O plano para você 
experimentar um dos serviços essenciais 
oferecidos, de acordo com as suas necessidades.
--------------------------------------------------
2 --> Pedal leve: Você gosta de pedalar e está 
buscando um plano de serviços intermediário? 
O Pedal leve da Porto é para você. 
--------------------------------------------------
3 --> Pedal elite: Conte com diversos serviços
capazes de elevar suas aventuras para o próximo
nível.
--------------------------------------------------
4 --> Saiba mais sobre nossos planos.
--------------------------------------------------
5 --> Voltar.
{linha(50)}""")
                    opc_plano = int(tratar_erro_num("Escolha uma opção: "))
                    match opc_plano:
                        case 1:
                            plano_selecionado = 'Pedal essencial'
                            break
                        case 2:
                            plano_selecionado = 'Pedal leve'
                            break
                        case 3:
                            plano_selecionado = 'Pedal elite'
                            break

                        # Exibe informações adicionais sobre os planos
                        case 4:
                            os.system('cls')
                            cabecalho("INFORMAÇÕES SOBRE PLANOS")
                            exibir_descricao_plano('Pedal essencial')
                            print('--------------------------------------------------')
                            exibir_descricao_plano('Pedal leve')
                            print('--------------------------------------------------')
                            exibir_descricao_plano('Pedal elite')
                            print(linha(50))
                            input("Pressione ENTER para voltar")

                        case 5:
                            cabecalho('VOLTANDO...')
                            sleep(1.5)
                            break
                        case _:
                            exibir_invalido()

                # Permite ao usuário redefinir seu plano
                else:
                    cabecalho(f"{plano_selecionado} selecionado.")
                    exibir_descricao_plano(plano_selecionado)
                    print(linha(50))
                    while True:
                        alterar_plano = input("Deseja alterar seu plano? [S/N]: ")
                        if alterar_plano.upper() == 'S' or alterar_plano.upper() == 'N':
                            break
                        else:
                            exibir_invalido()
                    if alterar_plano.upper() == 'S':
                        plano_selecionado = ""
                    else:
                        break

            os.system('cls')
            if plano_selecionado != "":
                cabecalho(f"{plano_selecionado} selecionado!!!")

        # Finaliza o programa
        case 4:

            # Exibe os dados que foram cadastrados
            os.system('cls')
            if d_pessoais_cadastrados:
                exibir_dados('DADOS PESSOAIS', dados['Dados Pessoais'])
                exibir_dados('ENDEREÇO', dados['Endereco'])
                sleep(1.0)
            else:
                dados_restantes.append('Cadastrar dados pessoais')
            if d_bike_cadastrados:
                exibir_dados('DADOS BIKE', dados['Dados Bike'])
                sleep(0.7)
                if possui_acessorio.upper() == 'S':
                    for i in range(quant_acessorio):
                        exibir_dados(f'ACESSÓRIO {i + 1}', dados[f'Acessório {i + 1}'])
                        sleep(0.7)
            else:
                dados_restantes.append('Cadastrar dados da bike')
            if plano_selecionado != "":
                cabecalho(f"{plano_selecionado} selecionado.")
                exibir_descricao_plano(plano_selecionado)
                print(linha(50))
                sleep(0.7)
            else:
                dados_restantes.append('Selecionar plano')

            # Caso o usuário tenha realizado todos os processos, a contratação será concluída
            if d_pessoais_cadastrados and d_bike_cadastrados and plano_selecionado != "":
                cabecalho("Contratação do seguro concluída!!!")
                break

            # Caso contrário, o usuário será informado dos dados faltantes
            # E poderá voltar ao programa e, se desejar, finalizar a contratação
            else:
                menu("Contratação incompleta. Ações em aberto:", dados_restantes)
                while True:
                    finalizar_programa = input("Deseja mesmo fechar o programa? [S/N]: ")
                    if finalizar_programa.upper() == 'S' or finalizar_programa.upper() == 'N':
                        break
                    else:
                        exibir_invalido()
                if finalizar_programa.upper() == 'S':
                    if d_pessoais_cadastrados:
                        delete_bd('cliente')
                        delete_bd('endereco')
                    if d_bike_cadastrados:
                        delete_bd('bike')
                        for i in range(quant_acessorio):
                            delete_bd('acessorio')
                    break
                else:
                    os.system('cls')
        case _:
            exibir_invalido()
cabecalho("Finalizando programa...")
cabecalho("Desenvolvido por: CycleX")

