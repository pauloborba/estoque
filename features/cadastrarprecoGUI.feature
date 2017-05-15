Feature: Cadastrar precos

  Scenario: Cadastrar valor para um item existente na loja
    Given eu vejo o item "Arroz" na lista de itens cadastrados
    Given eu vejo a loja "Extra" na lista de lojas cadastradas
    Given eu estou na pagina de cadastramento de precos
    When eu tento cadastrar o preco "5,00" do item "Arroz" na loja "Extra"
    Then eu vejo uma mensagem informando que o valor foi cadastrado corretamente
    Then eu vou para a pagina de precos cadastrados

  Scenario: Cadastrar valor para item que não está disponível na loja escolhido
  	Given eu estou na pagina de cadastramento de precos
  	Given eu vejo o item "Milho" na lista de itens cadastrados
  	Given eu vejo a loja "Bonzao" na lista de lojas cadastradas
  	Given a loja "Bonzao" nao possui o item "Milho"
  	When eu tento cadastrar o preco do item "Milho" na loja "Bonzao"
  	Then eu vejo uma mensagem informando que a loja "Bonzao" nao possui o item "Milho"
  	Then eu permaneco na pagina de cadastramento de precos

