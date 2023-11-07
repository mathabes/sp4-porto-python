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