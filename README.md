# estoque

## Como preparar o ambiente para o projeto via bash:
1. Instale o Python versão 2.7.x (2.7.9 no mínimo https://www.python.org/)
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
1. Va até a pasta `feature\driver\` e dê permissões de execução do geckodriver na pasta do seu respectivo sistema (Ex.: `chmod +x features/linux/geckodriver`)
1. Exporte o PATH do geckodriver do seu respectivo sistema (http://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path) (Ex.: `export PATH=$PATH:~/Documents/estoque/features/driver/linux`)
1. Rode o comando `python manage.py behave`

Uma janela do firefox vai abrir e rodar os testes

Referências:

- http://splinter.readthedocs.io/en/latest/
- https://github.com/behave/behave
- https://github.com/behave/behave-django
