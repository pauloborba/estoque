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
	  Given eu estou na pagina de cadastramento de precos
	  Given eu vejo o item "Arroz" na lista de itens cadastrados
	  Given eu vejo a loja "Extra" na lista de lojas cadastradas
	  When eu tento cadastrar o preco "5,00" do item "Arroz" na loja "Extra"
	  Then eu vou para a pagina de precos cadastrados
	  Then eu vejo o item "Arroz" com preco "5,00" na loja "Extra" na lista