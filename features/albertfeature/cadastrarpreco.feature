Feature: Cadastrar precos

  Scenario: Cadastrar valor para item que não está disponível na loja escolhido
  	Given eu estou na pagina de cadastramento de precos
  	Given eu vejo o item "Milho" na lista de itens cadastrados
  	Given eu vejo a loja "Bonzao" na lista de lojas cadastradas
  	Given a loja "Bonzao" nao possui o item "Milho"
  	When eu tento cadastrar o preco "3,00" para item "Milho" na loja "Bonzao"
  	Then eu vejo uma mensagem informando que a loja "oBonzao" nao possui o item "Milho"
  	Then eu permaneco na pagina de cadastramento de precos

  Scenario: Cadastrar valor para um item existente na loja
    Given eu vejo o item "Arroz" na lista de itens cadastrados
    Given eu vejo a loja "Extra" na lista de lojas cadastradas
    Given eu estou na pagina de cadastramento de precos
    When eu tento cadastrar o preco "5,00" do item "Arroz" na loja "Extra"
    Then eu vejo uma mensagem informando que o valor foi cadastrado corretamente
    Then eu vou para a pagina de precos cadastrados

  Scenario: Sobrescrever um preco já cadastrado
  	Given o item "Sabao" esta cadastrado no sistema com o preço "7,00" na loja "Merc"
  	Given o item "Feijao" esta cadastrado no sistema com o preço "10,00" na loja "Varejão"
  	When eu tento cadastrar o preco "5,00" do item "Sabao" na loja "Merc"
  	Then o sistema sobrescreve o preco do item "Sabao" na loja "Merc" para o valor "5,00"
  	And o item "Feijao" continua com o valor "10,00" na loja "Varejao"

  Scenario: Cancelar cadastramento de preco de produto
  	Given o item "Leite" esta cadastrada no sistema
  	Given a loja "Bom Preço" esta cadastrada no sistema
  	Given o preco "3,00" está para o item "Leite" na loja "Bom Preco"
  	Given o item "Leite" na loja "Bom Preco" ainda nao possui um preco
  	When eu tento cancelar o cadastramento do item "Leite" com o valor "3,00" na loja "Bom Preco"
  	Then a lista de preços nao é alterada
