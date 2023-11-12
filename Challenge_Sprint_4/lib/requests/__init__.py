# Importação dos módulos
import os
import cx_Oracle
import pandas as pd
cx_Oracle.init_oracle_client(lib_dir=r"C:\Program Files\instantclient_19_9")
import requests
from lib.subalgoritmos import *
def viacep_api(cep):
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

def update_bd(tabela: str, dado_antigo: str, novo_dado):
    try:
        consulta_max_id = f'SELECT MAX(id_{tabela}) FROM t_cyclex_{tabela}'
        inst_consulta.execute(consulta_max_id)
    
        # Obtém o máximo ID
        id_exclusao = inst_consulta.fetchone()[0]

        # Constroi a instrução de edição do registro com os novos dados
        alteracao = f""" UPDATE t_cyclex_{tabela} SET {dado_antigo} ='{novo_dado}' WHERE id_{tabela}={id_exclusao}"""
        inst_alteracao.execute(alteracao)
        conn.commit()
    except:
        print("\033[031m--> Erro na atualização dos dados.\033[m\n")
    else:
        print("\nDados ATUALIZADOS!")
    input("Presione ENTER")

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

def select_bd():
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
