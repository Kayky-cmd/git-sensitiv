import requests
import argparse
import re

print ("""
       
          ,___  ___  ______    __, ______ _ __   __,  ___  ______  ___  _,   _ ______
  /   / ( /  (  /      (   (  /   ( /  ) (    ( /  (  /    ( /  ( |  / (  /
 /  __   /     /        `.   /--   /  /   `.   /     /      /     | /    /--
(___/  _/_   _/       (___)(/____//  (_ (___)_/_   _/     _/_     |/   (/____/

       code by - d10x (Kayky)

""")


# Função para buscar uma palavra-chave ou dados sensíveis em um repositório
def scan_repository(keyword, repo_link, sensitive_mode=False, list_all=False):
    # Extrair o nome do usuário e nome do repositório do link
    repo_link = repo_link.rstrip('/')
    user, repo = repo_link.split('/')[-2:]

    # URL da API de busca do GitHub para encontrar arquivos em um repositório
    url = f'https://api.github.com/search/code?q=repo:{user}/{repo}'

    # Cabeçalho com token de acesso pessoal (substitua 'SEU_TOKEN' pelo seu token)
    headers = {
        'Authorization': 'token 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'
    }

    # Faça uma solicitação para buscar arquivos no repositório
    response = requests.get(url, headers=headers)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        try:
            data = response.json()
            items = data.get('items', [])
            for item in items:
                file_url = item['html_url']
                file_name = item['name']
                if list_all:
                    print(f'Arquivo: {file_name}')
                    if sensitive_mode and has_sensitive_data(repo_link, file_name):
                        print('(SENSÍVEL)')
                    print(f'URL: {file_url}')
                    print('-' * 40)
                if keyword and (keyword in file_name or (sensitive_mode and has_sensitive_data(repo_link, file_name))):
                    print(f'Arquivo: {file_name}')
                    if sensitive_mode and has_sensitive_data(repo_link, file_name):
                        print('(SENSÍVEL)')
                    print(f'URL: {file_url}')
                    print('-' * 40)
        except ValueError:
            print('Erro: Não foi possível obter os dados do repositório.')
    else:
        print(f'Erro: Não foi possível acessar o repositório (código {response.status_code})')

# Função para verificar se o conteúdo do arquivo contém dados sensíveis (exemplo)
def has_sensitive_data(repo_link, file_name):
    # Aqui você pode implementar lógica personalizada para verificar dados sensíveis
    # Esta é apenas uma demonstração simples
    sensitive_keywords = ['.sql', '.php', '.yaml']
    
    # Você pode fazer a verificação de acordo com o nome do arquivo ou usar a API de conteúdo do GitHub para obter o conteúdo
    # Aqui, estamos apenas verificando o nome do arquivo
    for keyword in sensitive_keywords:
        if keyword in file_name:
            return True
    return False

# Configurar os argumentos da linha de comando
parser = argparse.ArgumentParser(description='Git Varrer - Realizar uma busca em um repositório GitHub em busca de uma palavra-chave ou dados sensíveis')
parser.add_argument('-l', '--link', required=True, help='Link do repositório GitHub (exemplo: https://github.com/nome_do_usuario/nome_do_repositorio)')
parser.add_argument('-k', '--keyword', help='Palavra-chave a ser procurada nos arquivos do repositório')
parser.add_argument('-s', '--sensitive', action='store_true', help='Ativar modo de busca de dados sensíveis')
parser.add_argument('-all', action='store_true', help='Listar todos os arquivos no repositório')

args = parser.parse_args()

# Chame a função de busca de repositório com os parâmetros fornecidos
scan_repository(args.keyword, args.link, args.sensitive, args.all)