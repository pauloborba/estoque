Feature: Gerar lista de compras de uma determinada loja que possui seções      

  #Controlador

  #Cenario 1:
  Scenario: Cria lista de Loja específica que possui seções
    Given a loja “Mercadinho” está registrada no sistema
    And as seções “Bebidas” e “Frios” foram cadastradas em “Mercadinho”
    And os produtos “Mortadela” e “Queijo Coalho” estão cadastrados no estoque
    And os produtos “Mortadela” e “Queijo Coalho” estão em falta no estoque
    And o produto “Mortadela” está associado com a seção “Frios” de “Mercadinho” com preço de R$ "2.45"
    And o produto “Queijo Coalho” está associado com a seção “Frios” de “Mercadinho” com preço de R$ "5.50"
      When eu solicito a criação da lista exclusiva para “Mercadinho”
        Then o arquivo “Mercadinho.pdf” é enviado

  #Cenario 2:
  Scenario: Cria lista de Loja específica que possui seções quando não há itens em falta
    Given a loja “Mercadinho” está registrada no sistema
    And existem no sistema “0” produtos em falta
      When eu solicito a criação da lista exclusiva para “Mercadinho”
      Then o arquivo “mercadinho.pdf” não é enviado