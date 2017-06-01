Feature: Gerar lista de compras de uma determinada loja que possui seções      


  #Controlador

  #Cenario 1:
  Scenario: Cria lista de loja
    Given a loja "Mercadinho" está registrada no sistema
    And as seções "Bebidas" e "Frios" foram cadastradas em "Mercadinho"
    And os produtos "Mortadela" e "Queijo Coalho" estão cadastrados no estoque
    And os produtos "Mortadela" e "Queijo Coalho" estão em falta no estoque
    And o produto "Mortadela" está associado com a seção "Frios" de "Mercadinho" com preço de R$ "2.45"
    And o produto "Queijo Coalho" está associado com a seção "Frios" de "Mercadinho" com preço de R$ "5.50"
      When eu solicito a criação da lista exclusiva para "Mercadinho"
        Then o arquivo "Mercadinho.pdf" é enviado

  #Cenario 2:
  Scenario: Cria lista de loja quando não há itens em falta
    Given a loja "Mercadinho" está registrada no sistema
    And existem no sistema "0" produtos em falta
      When eu solicito a criação da lista exclusiva para "Mercadinho"
      Then o arquivo "Mercadinho.pdf" não é enviado



  #GUI


  #Cenario 1:
  Scenario: Cria lista de Loja específica que possui seções
    Given a loja "Mercadinho" foi registrada no sistema
    And a loja "Mercadinho" tem 3 seções cadastradas: "Cereais", "Frios" e "Limpeza", nessa ordem
    And os produtos "Aveia", "Vassoura", "Mortadela" e "Queijo" foram cadastrados
    And para a seção "Limpeza" em "Mercadinho" foi associado o produto "Vassoura" com preço "3.40"
    And para a seção "Frios" em "Mercadinho" foram associados os seguintes produtos: "Mortadela" com preço "2.45" e "Queijo" com preço "5.50"
    And para a seção "Cereais" em "Mercadinho" foi associado o produto "Aveia" com preço "4.99"
    And vejo na página "generate_list" que os seguintes produtos "Vassoura", "Mortadela" e "Queijo" estão em falta no estoque
    And estou na página "newListByStore"
      When seleciono a loja "Mercadinho" na lista de lojas
      And seleciono a opção "baixar"
        Then vejo que um arquivo pdf de nome "Mercadinho.pdf" foi baixado
        #And vejo uma lista com os itens "Vassoura - R$ 3.40", "Mortadela - R$ 2.45" e "Queijo - R$ 5.50"
        #And os itens "Mortadela" e "Queijo" aparecem relacionados com a seção "Frios"
        #And "Vassoura" aparece na seção "Limpeza"
        #And vejo que a seção "Limpeza" aparece antes de "Frios"
        #And no final da lista vejo o preço total de R$ "11.35".


  #Cenario 2:
  Scenario: Cria lista de loja quando não há itens em falta
    Given observo na página "generate_list" que não há itens em falta
    And estou na página "newListByStore"
    And a loja "Mercadinho" está registrada no sistema
      When seleciono a loja "Mercadinho" na lista de lojas
      And seleciono a opção "baixar"
        Then vejo uma mensagem informando "Lista não foi criada. Não existem itens em falta para essa loja"