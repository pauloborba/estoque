# estoque

## Como preparar o ambiente para o projeto via bash:
1. Instale o Python versão 2.7.x (2.7.9 no mínimo https://renoirboulanger.com/blog/2015/04/upgrade-python-2-7-9-ubuntu-14-04-lts-making-deb-package/)
1. Instale o bower (https://docs.npmjs.com/getting-started/installing-node)
1. Clone o projeto
1. Vá ao diretório raiz do projeto
1. Rode o comando `bower install`
1. Rode o comando `pip install -r requirements.txt`
1. Rode o comando `python manage.py migrate` (Obs.: toda vez que uma migração nova for criada rodar esse comando)

## Como rodar o projeto via bash:
1. Rode o comando `python manage.py runserver`

Um servidor local que atende em localhost:8000 deve estar sendo rodado em sua maquina.

## Como rodar os testes do projeto via bash:
1. Em [features/environment.py](/features/environment.py) escolha o browser que irá executar os testes de GUI
2. Baixe o *path* do browser escolhido:
    1. [Firefox](https://github.com/mozilla/geckodriver/releases)
    2. [Chrome](https://chromedriver.storage.googleapis.com/index.html?path=2.29/)
3. Copie o arquivo baixado para 'usr/local/bin'
4. Rode o comando `python manage.py behave`

Referências:

- http://splinter.readthedocs.io/en/latest/
- https://github.com/behave/behave
- https://github.com/behave/behave-django
