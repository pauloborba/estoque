Feature: Cadastrar preco

  Scenario: Sobrescrever um preco já cadastrado
    Given a loja "Merc" esta cadastrada no sistema
    Given a secao "Limpeza" esta cadastrada no sistema para a loja "Merc"
  	Given o produto "Sabao" esta cadastrado no sistema com o preço "7.00" na secao "Limpeza" da loja "Merc"
  	  When eu tento cadastrar o preco "5.00" do produto "Sabao" na secao "Limpeza" da loja "Merc"
  	    Then o sistema sobrescreve o preco do produto "Sabao" na loja "Merc" para o valor "5.00"

  Scenario: Criar preco com base no item e no supermercado
    Given a loja "Extra" esta cadastrada no sistema
    Given a secao "Bebidas" esta cadastrada no sistema para a loja "Extra"
    Given o produto "Agua" esta cadastrado no sistema
    Given nao existe preco cadastrado para o produto "Agua" na secao "Bebidas" da loja "Extra"
      When eu tento cadastrar o preco "3.00" do produto "Agua" na secao "Bebidas" da loja "Extra"
        Then o sistema cadastra corretamente o preco "3.00" para o produto "Agua" na secao "Bebidas" da loja "Extra"