Feature: Cadastrar preco

  Scenario: Sobrescrever um preco já cadastrado
    Given a loja "Merc" esta cadastrada no sistema
    Given a secao "Limpeza" esta cadastrada no sistema para a loja "Merc"
  	Given o item "Sabao" esta cadastrado no sistema com o preço "7.00" na secao "Limpeza" da loja "Merc"
  	  When eu tento cadastrar o preco "5.00" do item "Sabao" na secao "Limpeza" da loja "Merc"
  	    Then o sistema sobrescreve o preco do item "Sabao" na loja "Merc" para o valor "5.00"