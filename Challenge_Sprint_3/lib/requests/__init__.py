# Importação dos módulos
import os
import cx_Oracle
import pandas as pd
cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\instantclient_19_9")
import requests
from lib.subalgoritmos import *
def viacep_api(cep):
    try:
        endereco = {'CEP': '', 'Número': '', 'Logradouro': '', 'Complemento': '', 'Bairro': '', 'Localidade': '', 'UF': ''}
        requisicao = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        requisicao_dic = requisicao.json()
        
        endereco['CEP'] = requisicao_dic['cep']
        
        endereco['Logradouro'] = requisicao_dic['logradouro']
        if endereco['Logradouro'] == "":
            endereco['Logradouro'] = validacoes('Logradouro')
        
        endereco['Complemento'] = requisicao_dic['complemento']
        if endereco['Complemento'] == "":
            endereco['Complemento'] = validacoes('Complemento(opcional)')
        
        endereco['Número'] = tratar_erro_num('Número do Logradouro: ')
        
        endereco['Bairro'] = requisicao_dic['bairro']
        if endereco['Bairro'] == "":
            endereco['Bairro'] = validacoes('Bairro')

        endereco['Localidade'] = requisicao_dic['localidade']
        
        endereco['UF'] = requisicao_dic['uf']
    except:
        print("\033[031m--> ERRO: Falha na conexão com a API.\033[m\n")
    return endereco

def insert_bd(tabela: str, dados: dict):
    try:
        if tabela == 'cliente':
            # Monta a instrução SQL de cadastro em uma string
            cadastro = f""" INSERT INTO t_cyclex_{tabela}  (nome, email, telefone, cpf, cep) 
            VALUES ('{dados['Nome']}', '{dados['Email']}', '{dados['Telefone']}', '{dados['CPF']}', '{dados['CEP']}') """
        
        elif tabela == 'endereco':
            # Monta a instrução SQL de cadastro em uma string
            cadastro = f""" INSERT INTO t_cyclex_{tabela}  (numero, logradouro, complemento, bairro, localidade, uf) 
            VALUES ('{dados['Número']}', '{dados['Logradouro']}', '{dados['Complemento']}',
            '{dados['Bairro']}', '{dados['Localidade']}', '{dados['UF']}') """
        
        elif tabela == 'bike':
            # Monta a instrução SQL de cadastro em uma string
            cadastro = f""" INSERT INTO t_cyclex_{tabela}  (marca, modelo, chassi, valor) 
            VALUES ('{dados['Marca']}','{dados['Modelo']}', '{dados['Chassi']}', '{dados['Valor']}') """
        
        else:
            # Monta a instrução SQL de cadastro em uma string
            cadastro = f""" INSERT INTO t_cyclex_{tabela}  (tipo_acessorio, marca_acessorio, 
            modelo_acessorio, valor_acessorio) 
            VALUES ('{dados['Tipo do acessório']}','{dados['Marca do acessório']}', '{dados['Modelo do acessório']}', 
            '{dados['Preço do acessório']}') """
        
        # Executa e grava o Registro na Tabela
        inst_cadastro.execute(cadastro)
        conn.commit()
    except:
        print("\033[031m--> Erro no cadastro dos dados.\033[m\n")
    else:
        print("\nDados GRAVADOS")
        input("Presione ENTER")

def update_bd():
    try:
        print("----- ALTERAR DADOS DO PET -----\n")
        lista_dados = [] # Lista para captura de dados da tabela
        pet_id = int(input(margem + "Escolha um Id: ")) # Permite o usuário escolher um Pet pelo id
                    
        # Constroi a instrução de consulta para verificar a existencia ou não do id
        consulta = f""" SELECT * FROM petshop WHERE id =
        {pet_id}"""
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        # Preenche a lista com o registro encontrado (ou não)
        for dt in data:
            lista_dados.append(dt)
                    
        # analisa se foi encontrado algo
        if len(lista_dados) == 0: # se não há o id
            print(f"Não há um pet cadastrado com o ID = {pet_id}")
            input("\nPressione ENTER")
        else:
            # Captura os novos dados
            novo_tipo = input(margem + "Digite um novo tipo: ")
            novo_nome = input(margem + "Digite um novo nome: ")
            nova_idade = input(margem + "Digite uma nova idade: ")
            # Constroi a instrução de edição do registro com os novos dados
            alteracao = f"""
            UPDATE petshop SET tipo_pet='{novo_tipo}',
            nome_pet='{novo_nome}', idade='{nova_idade}' WHERE id={pet_id}
            """
            inst_alteracao.execute(alteracao)
            conn.commit()
    except ValueError:
        print("Digite um número na idade!")
    except:
        print("Erro na transação do BD")
    else:
        print("\nDados ATUALIZADOS!")
    input("Presione ENTER")

def delete_bd(tabela):
    try:
        lista_dados = [] # Lista para captura de dados do Banco

        # Monta a instrução SQL de seleção de todos os registros da tabela
        inst_consulta.execute(f'SELECT * FROM {tabela}')

        # Captura todos os registros da tabela e armazena no objeto data
        data = inst_consulta.fetchall()

        # Insere os valores da tabela na Lista
        for dt in data:
            lista_dados.append(dt)

        # ordena a lista
        lista_dados = sorted(lista_dados)

        if tabela == 'cliente':
            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados,
            columns=['Id', 'Nome', 'Email', 'Telefone', 'CPF', 'CEP'], index='Id')
        if tabela == 'endereco':
            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados,
            columns=['Id', 'Número', 'Logradouro', 'Complemento', 'Bairro', 'Localidade', 'UF'], index='Id')
        if tabela == 'bike':
            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados,
            columns=['Id', 'Marca', 'Modelo', 'Chassi', 'Valor'], index='Id')
        if tabela == 'acessorio':
            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados,
            columns=['Id', 'Marca do acessório', 'Modelo do acessório', 'Chassi do acessório', 'Valor do acessório'], index='Id')

        lista_id = dados_df['Id'].tolist()
        id_exclusao = max(lista_id)

        exclusao = f"DELETE FROM t_cyclex_cliente WHERE id={id_exclusao}"
        # Executa a instrução e atualiza a tabela
        inst_exclusao.execute(exclusao)
        conn.commit()
    except:
        print("\033[031m--> Erro ao deletar os dados.\033[m\n")
    print("\nPet APAGADO!") # Exibe mensagem caso haja sucesso
    input("Pressione ENTER") # Pausa o loop para a leitura da mensagem

def select_bd():
    print("----- LISTAR PETs -----\n")
    lista_dados = [] # Lista para captura de dados do Banco

    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute('SELECT * FROM petshop')

    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista_dados.append(dt)

    # ordena a lista
    lista_dados = sorted(lista_dados)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    dados_df = pd.DataFrame.from_records(lista_dados,
    columns=['Id', 'Tipo', 'Nome', 'Idade'], index='Id')

    # Verifica se não há registro através do dataframe
    if dados_df.empty:
        print(f"Não há um Pets cadastrados!")
    else:
        print(dados_df) # Exibe os dados selecionados da tabela
    print("\nLISTADOS!")
    input("Pressione ENTER")


# Conectando com o banco de dados
try:
    # Conecta o servidor
    dsnStr = cx_Oracle.makedsn("oracle.fiap.com.br", "1521",
                                "ORCL")
    # Efetua a conexão com o Usuário
    conn = cx_Oracle.connect(user='RM98502', password="090405",
                                dsn=dsnStr)
    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    # Informa o erro
    print(f"\033[031mErro: {e}\033[m\n")
    # Flag para não executar a Aplicação
    conexao = False
else:
    conexao = True
