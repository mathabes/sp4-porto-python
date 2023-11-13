# Importação dos módulos
import requests
from lib.subalgoritmos import *
import os
import pandas as pd
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\instantclient_19_9")

def viacep_api(cep):
    endereco = {'Número': '', 'Logradouro': '', 'Complemento': '', 'Bairro': '', 'Localidade': '', 'UF': ''}
    requisicao = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    requisicao_dic = requisicao.json()

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

def update_bd(tabela: str, opc_menu_alterar: int, novo_dado):
    dado_antigo = ''
    match opc_menu_alterar:
        case 1:
            if tabela == 'cliente':
                dado_antigo = 'nome'
            elif tabela == 'endereco':
                dado_antigo = 'numero'
            elif tabela == 'bike':
                dado_antigo = 'marca'
            else:
                dado_antigo = 'tipo do acessorio'
        case 2:
            if tabela == 'cliente':
                dado_antigo = 'email'
            elif tabela == 'endereco':
                dado_antigo = 'logradouro'
            elif tabela == 'bike':
                dado_antigo = 'modelo'
            else:
                dado_antigo = 'marca do acessorio'
        case 3:
            if tabela == 'cliente':
                dado_antigo = 'telefone'
            elif tabela == 'endereco':
                dado_antigo = 'complemento'
            elif tabela == 'bike':
                dado_antigo = 'chassi'
            else:
                dado_antigo = 'modelo do acessorio'
        case 4:
            if tabela == 'cliente':
                dado_antigo = 'cpf'
            elif tabela == 'endereco':
                dado_antigo = 'bairro'
            elif tabela == 'bike':
                dado_antigo = 'valor'
            else:
                dado_antigo = 'valor do acessorio'
        case 5:
            if tabela == 'cliente':
                dado_antigo = 'cep'
            else:
                dado_antigo = 'localidade'
        case 6:
            dado_antigo = 'uf'

    consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_cyclex_{tabela}'
    inst_consulta.execute(consulta_max_id)

        # Obtém o máximo ID
    id_exclusao = inst_consulta.fetchone()[0]

        # Constroi a instrução de edição do registro com os novos dados
    alteracao = f""" UPDATE t_cyclex_{tabela} SET {dado_antigo} ='{novo_dado}' WHERE id_{tabela}={id_exclusao}"""
    inst_alteracao.execute(alteracao)
    conn.commit()

def delete_bd(tabela):
    # Monta a instrução SQL para obter o máximo ID
    consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_cyclex_{tabela}'
    inst_consulta.execute(consulta_max_id)

    # Obtém o máximo ID
    id_exclusao = inst_consulta.fetchone()[0]

    if id_exclusao is not None:
        # Constrói a instrução SQL para exclusão usando parâmetros vinculados
        exclusao = f"DELETE FROM t_cyclex_{tabela} WHERE Id_{tabela} = :id"
        inst_exclusao.execute(exclusao, {'id': id_exclusao})
        conn.commit()
    else:
        print(f"Nenhum registro encontrado para exclusão em t_cyclex_{tabela}.")

def select_bd(tabela) -> dict:
    lista_dados = []  # Lista para captura de dados do Banco
    consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_cyclex_{tabela}'
    inst_consulta.execute(consulta_max_id)
    ultima_ocorrencia = inst_consulta.fetchone()[0]

    if tabela == 'cliente':
        exibir_colunas = ['Nome', 'Email', 'Telefone', 'CPF', 'CEP']
        colunas_select = 'nome, email, telefone, cpf, cep'
    if tabela == 'endereco':
        exibir_colunas = ['Número', 'Logradouro', 'Complemento', 'Bairro', 'Localidade', 'UF']
        colunas_select = 'numero, logradouro, complemento, bairro, localidade, uf'
    if tabela == 'bike':
        exibir_colunas = ['Marca', 'Modelo', 'Chassi', 'Valor']
        colunas_select = 'marca, modelo, chassi, valor'

    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute(f'''SELECT {colunas_select} FROM t_cyclex_{tabela} 
                          WHERE id_{tabela} = {ultima_ocorrencia}
    ''')

    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista_dados.append(dt)

    # ordena a lista
    lista_dados = sorted(lista_dados)
    
    # Cria um dicionário vazio
    dados_dict = {}

    # Adiciona elementos ao dicionário usando um laço de repetição
    for i in range(len(exibir_colunas)):
        if i < len(data[0]):  # Certifica-se de que o índice não ultrapasse o comprimento da lista
            dados_dict[exibir_colunas[i]] = data[0][i]

    return dados_dict

def select_bd_acessorios(acessorio_escolhido):
    lista_dados = []  # Lista para captura de dados do Banco
    exibir_colunas = ['Tipo', 'Marca', 'Modelo', 'Preço']
    consulta_max_id = f'SELECT MAX(id_acessorio) FROM t_cyclex_acessorio'
    inst_consulta.execute(consulta_max_id)
    ultima_ocorrencia = inst_consulta.fetchone()[0]

    # Monta a instrução SQL de seleção de todos os registros da tabela
    inst_consulta.execute(f'''SELECT tipo_acessorio, marca_acessorio, modelo_acessorio, valor_acessorio FROM t_cyclex_acessorio 
        WHERE id_acessorio = {ultima_ocorrencia - acessorio_escolhido}''')
    
    # Captura todos os registros da tabela e armazena no objeto data
    data = inst_consulta.fetchall()

    # Insere os valores da tabela na Lista
    for dt in data:
        lista_dados.append(dt)

    # ordena a lista
    lista_dados = sorted(lista_dados)
    
    # Cria um dicionário vazio
    dados_dict = {}

    # Adiciona elementos ao dicionário usando um laço de repetição
    for i in range(len(exibir_colunas)):
        if i < len(data[0]):  # Certifica-se de que o índice não ultrapasse o comprimento da lista
            dados_dict[exibir_colunas[i]] = data[0][i]

    return dados_dict

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
