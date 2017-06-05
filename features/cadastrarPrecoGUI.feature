Feature: Cadastrar preco

    Scenario: Cancelar cadastramento de preco
    Given o item "Laranja" esta cadastrado no sistema
    Given a secao "Frutas" esta cadastrada para a loja "Hiper"
  	Given eu estou na pagina de cadastramento de precos
    Given eu seleciono o item "Laranja" na lista de itens cadastrados
    Given eu seleciono a secao "Frutas" da loja "Hiper" na lista de secoes
  	Given eu preencho o campo preco com valor "3.00"
  	Given o item "Laranja" na loja "Hiper" ainda nao possui um preco
  	When eu tento cancelar o cadastramento do item "Laranja" com o valor "3,00" na loja "Hiper"
  	Then eu estou na pagina de precos cadastrados
    Then a lista de precos nao foi alterada

    Scenario: Tentar cadastrar preco sem digitar o valor
    Given o item "Treloso" esta cadastrado no sistema
    Given a secao "Lanches" esta cadastrada para a loja "Extra"
    Given eu estou na pagina de cadastramento de precos
    Given eu seleciono o item "Treloso" na lista de itens cadastrados
    Given eu seleciono a secao "Lanches" da loja "Extra" na lista de secoes
    Given o campo de cadastramento de preco esta vazio
    When eu tento cadastrar preco para o item "Treloso" na loja "Extra"
    Then eu permaneco na pagina de cadastramento de precos
    Then eu vejo uma mensagem informando que falta inserir um preco
