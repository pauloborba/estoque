Feature: Generate List of selected stores

  Scenario: Retirar um supermercado da lista e gerar lista

    Given Os produtos Feijao, Lasanha estao cadastrados no sistema com quantidade 3 e quantidade minima 5
	And A loja Carrefour esta cadastrada com a sessao Geral e a loja Extra esta cadastrada
	And A loja Carrefour possui Feijao na sessao Geral com o preco 2.50 e Lasanha na sessao Geral com o preco 6.00
	And So ha esses 2 itens cadastrados
	When Eu navego para a pagina gerar lista de lojas
	And Eu desmarco a loja Extra
	And Eu seleciono a opcao gerar lista
	Then Eu recebo um arquivo e vejo escrito Carrefour e vejo Feijao e vejo Lasanha e nao vejo Extra

