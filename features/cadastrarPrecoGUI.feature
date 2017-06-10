Feature: Cadastrar preco

    Scenario: Cancelar cadastramento de preco
    Given o item "Laranja" esta cadastrado no sistema
    Given a secao "Frutas" esta cadastrada para a loja "Hiper"
  	Given eu estou na pagina de cadastramento de precos
  	Given o item "Laranja" na loja "Hiper" ainda nao possui um preco
    When eu seleciono o item "Laranja" na lista de itens cadastrados
    When eu seleciono a secao "Frutas" da loja "Hiper" na lista de secoes
    When eu preencho o campo preco com valor "3.00"
  	When eu tento cancelar o cadastramento do item "Laranja" com o valor "3,00" na loja "Hiper"
  	Then eu estou na pagina de precos cadastrados
    Then a lista de precos nao foi alterada

    Scenario: Tentar cadastrar preco sem digitar o valor
    Given o item "Treloso" esta cadastrado no sistema
    Given a secao "Lanches" esta cadastrada para a loja "Extra"
    Given eu estou na pagina de cadastramento de precos
    Given o campo de cadastramento de preco esta vazio
    When eu seleciono o item "Treloso" na lista de itens cadastrados
    When eu seleciono a secao "Lanches" da loja "Extra" na lista de secoes
    When eu tento cadastrar preco para o item "Treloso" na loja "Extra"
    Then eu permaneco na pagina de cadastramento de precos
    Then eu vejo uma mensagem informando que falta inserir um preco

    Scenario: Visualizar lista de historico
    Given o item "Bolo" esta cadastrado no sistema
    Given a secao "Massas" esta cadastrada para a loja "Preco Legal"
    Given o preço "25.00" esta cadastrado no sistema para o produto "Bolo" na secao "Massas" da loja "Preco Legal"
    Given eu estou na pagina principal
    When eu seleciono a opcao de ver historico
    Then eu estou na pagina de historicos
    Then eu vejo o produto "Bolo" no historico de precos

    Scenario: Nenhum historico cadastrado
    Given nenhum produto, loja ou preco esta cadastrado no sistema
    Given eu estou na pagina principal
    When eu seleciono a opcao de ver historico
    Then eu estou na pagina de historicos
    Then a lista de historico esta vazia
