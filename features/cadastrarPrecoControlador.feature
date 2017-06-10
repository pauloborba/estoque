Feature: Cadastrar preco

  Scenario: Sobrescrever um preco já cadastrado
    Given a loja "Merc" esta cadastrada no sistema
    Given a secao "Limpeza" esta cadastrada no sistema para a loja "Merc"
  	Given o preço "7.00" esta cadastrado no sistema para o produto "Sabao" na secao "Limpeza" da loja "Merc"
  	  When eu tento cadastrar o preco "5.00" do produto "Sabao" na secao "Limpeza" da loja "Merc"
  	    Then o sistema sobrescreve o preco do produto "Sabao" na loja "Merc" para o valor "5.00"

  Scenario: Criar preco com base no item e no supermercado
    Given a loja "Extra" esta cadastrada no sistema
    Given a secao "Bebidas" esta cadastrada no sistema para a loja "Extra"
    Given o produto "Agua" esta cadastrado no sistema
    Given nao existe preco cadastrado para o produto "Agua" na secao "Bebidas" da loja "Extra"
      When eu tento cadastrar o preco "3.00" do produto "Agua" na secao "Bebidas" da loja "Extra"
        Then o sistema cadastra corretamente o preco "3.00" para o produto "Agua" na secao "Bebidas" da loja "Extra"


  #Segunda iteracao
  Scenario: Criacao de historico de cadastramento de preco
    Given a loja "Americanas" esta cadastrada no sistema
    Given a secao "Tecnologia" esta cadastrada no sistema para a loja "Americanas"
    Given o produto "MP3" esta cadastrado no sistema
    Given nao existe preco cadastrado para o produto "MP3" na secao "Tecnologia" da loja "Americanas"
      When eu tento cadastrar o preco "100.00" do produto "MP3" na secao "Tecnologia" da loja "Americanas"
        Then o sistema cadastra corretamente o preco "100.00" para o produto "MP3" na secao "Tecnologia" da loja "Americanas"
        Then e criado um historico de precos para o produto "MP3" na secao "Tecnologia" da loja "Americanas"

  Scenario: Verificar o item que teve mais alteracoes de preco
    Given a loja "Atacadao" esta cadastrada no sistema
    Given a secao "Brinquedos" esta cadastrada no sistema para a loja "Atacadao"
    Given o produto "Uno" esta cadastrado no sistema
    Given o produto "Domino" esta cadastrado no sistema
    Given o preço "15.00" esta cadastrado no sistema para o produto "Uno" na secao "Brinquedos" da loja "Atacadao"
    Given o preço "8.00" esta cadastrado no sistema para o produto "Domino" na secao "Brinquedos" da loja "Atacadao"
    Given nao existe outros precos cadastrados alem dos precos para os items "Uno" e "Domino"
      When eu sobrescrevo o preco para o produto "Uno" na secao "Brinquedos" da loja "Atacadao" para "18.00"
        Then o sistema verifica que o preco para o produto "Uno" na secao "Brinquedos" da loja "Atacadao" e o que possui mais historicos