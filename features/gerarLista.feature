Feature: Gerar lista das lojas selecionadas

  Scenario: Retirar um supermercado da lista e gerar lista

    Given Os produtos Feijao, Lasanha estao cadastrados no sistema com quantidade 3 e quantidade minima 5
	And A loja Carrefour esta cadastrada
	And A loja Extra esta cadastrada
	And A loja Carrefour possui a sessao Geral
	And A loja Carrefour possui Feijao na sessao Geral com o preco 2.50 e Lasanha na sessao Geral com o preco 6.00
	And So ha esses 2 itens cadastrados
	When Eu navego para a pagina gerar lista de lojas
	And Eu desmarco a loja Extra
	And Eu seleciono a opcao gerar lista
	Then Eu recebo um arquivo e vejo escrito Carrefour e vejo Feijao e vejo Lasanha e nao vejo Extra

  Scenario: Totalizar o preço gasto em uma loja

  	Given Os produtos Carne, Macarrao estao cadastrados no sistema com quantidade 3 e quantidade minima 5
  	And Os produtos Suco, Coca estao cadastrados no sistema com quantidade 2 e quantidade minima 4
	And A loja Wallmart esta cadastrada
	And A loja Wallmart possui a sessao Comidas
	And A loja Wallmart possui a sessao Bebidas
	And A loja Wallmart possui Carne na sessao Comidas com o preco 25.50 e Macarrao na sessao Comidas com o preco 8.00
	And A loja Wallmart possui Suco na sessao Bebidas com o preco 4.25 e Coca na sessao Bebidas com o preco 6.00
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then Eu recebo um arquivo e vejo escrito Total Wallmart 43.75

  Scenario: Totalizar o preço da lista

  	Given Os produtos Carne, Macarrao estao cadastrados no sistema com quantidade 3 e quantidade minima 5
  	And Os produtos Suco, Coca estao cadastrados no sistema com quantidade 2 e quantidade minima 4
	And A loja Wallmart esta cadastrada
	And A loja Extra esta cadastrada
	And A loja Wallmart possui a sessao Comidas
	And A loja Wallmart possui a sessao Bebidas
	And A loja Extra possui a sessao Bebidas
	And A loja Wallmart possui Carne na sessao Comidas com o preco 25.50 e Macarrao na sessao Comidas com o preco 8.00
	And A loja Wallmart possui Suco na sessao Bebidas com o preco 4.25 e Coca na sessao Bebidas com o preco 6.00
	And A loja Extra possui Suco na sessao Bebidas com o preco 5.00 e Coca na sessao Bebidas com o preco 5.00
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then Eu recebo um arquivo e vejo escrito Total 53.75

  Scenario: Tentar Gerar Lista sem nenhuma loja selecionada

    Given Os produtos Feijao, Lasanha estao cadastrados no sistema com quantidade 3 e quantidade minima 5
	And A loja Carrefour esta cadastrada
	And A loja Extra esta cadastrada
	And A loja Carrefour possui a sessao Geral
	And A loja Carrefour possui Feijao na sessao Geral com o preco 2.50 e Lasanha na sessao Geral com o preco 6.00
	When Eu navego para a pagina gerar lista de lojas
	And Eu desmarco a loja Extra
	And Eu desmarco a loja Carrefour
	And Eu seleciono a opcao gerar lista
	Then Eu nao recebo o arquivo com a lista

  Scenario: Tentar Gerar Lista com todos os itens com quantidade acima da quantidade minima

    Given Os produtos Feijao, Lasanha estao cadastrados no sistema com quantidade 6 e quantidade minima 5
	And A loja Carrefour esta cadastrada
	And A loja Extra esta cadastrada
	And A loja Carrefour possui a sessao Geral
	And A loja Carrefour possui Feijao na sessao Geral com o preco 2.50 e Lasanha na sessao Geral com o preco 6.00
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then Eu nao recebo o arquivo com a lista

  Scenario: Tentar Gerar Lista sem lojas cadastradas

    Given Nao ha lojas cadastradas no sistema
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then Eu nao recebo o arquivo com a lista

  Scenario: Gerar Lista não altera a quantidade atual dos itens cadastrados

	Given Os produtos Leite, Iogurte estao cadastrados no sistema com quantidade 8 e quantidade minima 10
  	And Os produtos Detergente, Bucha estao cadastrados no sistema com quantidade 4 e quantidade minima 5
	And A loja Bom Preço esta cadastrada
	And A loja Bom Preço possui a sessao Limpeza
	And A loja Bom Preço possui a sessao Laticinios
	And A loja Bom Preço possui Detergente na sessao Limpeza com o preco 3.50 e Bucha na sessao Limpeza com o preco 4.00
	And A loja Bom Preço possui Leite na sessao Laticinios com o preco 5.00 e Iogurte na sessao Laticinios com o preco 3.00
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then A quantidade do item Leite se mantem 8
	And A quantidade do item Iogurte se mantem 8
	And A quantidade do item Detergente se mantem 4
	And A quantidade do item Bucha se mantem 4

  Scenario: Gerar Lista não altera o preço dos itens cadastrados

	Given Os produtos Fralda, Talco estao cadastrados no sistema com quantidade 7 e quantidade minima 8
	And A loja Pão de Açucar esta cadastrada
	And A loja Pão de Açucar possui a sessao Utilitarios
	And A loja Pão de Açucar possui Fralda na sessao Utilitarios com o preco 11.00 e Talco na sessao Utilitarios com o preco 7.50
	When Eu navego para a pagina gerar lista de lojas
	And Eu seleciono a opcao gerar lista
	Then O preco do item Fralda na loja Pão de Açucar se mantem 11.00
	And O preco do item Talco na loja Pão de Açucar se mantem 7.50

  