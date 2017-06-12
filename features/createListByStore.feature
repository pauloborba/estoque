Feature: Gerar lista de compras de uma determinada loja que possui seções      


#  #Controlador
#
#
#  #Cenario 1:
#  Scenario: Cria lista de loja
#    Given a loja "Mercadinho" está registrada no sistema
#    And as seções "Bebidas" e "Frios" foram cadastradas em "Mercadinho"
#    And os produtos "Mortadela" e "Queijo Coalho" estão cadastrados no estoque
#    And os produtos "Mortadela" e "Queijo Coalho" estão em falta no estoque
#    And para a seção "Frios" em "Mercadinho" foi associado o produto "Mortadela" com preço "2.45"
#    And para a seção "Frios" em "Mercadinho" foi associado o produto "Queijo Coalho" com preço "5.5"
#      When eu solicito a criação da lista exclusiva para "Mercadinho"
#        Then o arquivo "ListaLoja.pdf" é enviado
#        And a seção "Frios" aparece com os itens "Queijo Coalho" "5.5" e "Mortadela" "2.45"
#        And no final do arquivo aparece o total de "7.95"
#
#  #Cenario 2:
#  Scenario: Cria lista de loja que não possui itens em falta
#    Given a loja "Mercadinho" está registrada no sistema
#    And existem no sistema "0" produtos em falta
#      When eu solicito a criação da lista exclusiva para "Mercadinho"
#        Then o arquivo "ListaLoja.pdf" não é enviado
#
#
#  #GUI
#
#
#  #Cenario 3:
#  Scenario: Cria lista de Loja com seções ordenadas pela GUI
#    Given a loja "Mercadinho" está registrada no sistema
#    And a loja "Mercadinho" tem 3 seções cadastradas: "Cereais", "Frios" e "Limpeza", nessa ordem
#    And os produtos "Aveia" e "Vassoura" estão cadastrados no estoque
#    And os produtos "Mortadela" e "Queijo" estão cadastrados no estoque
#    And os produtos "Mortadela" e "Queijo" estão em falta no estoque
#    And o produto "Vassoura" está em falta no estoque
#    And para a seção "Limpeza" em "Mercadinho" foi associado o produto "Vassoura" com preço "3.4"
#    And para a seção "Frios" em "Mercadinho" foram associados os seguintes produtos: "Mortadela" com preço "2.45" e "Queijo" com preço "5.5"
#    And para a seção "Cereais" em "Mercadinho" foi associado o produto "Aveia" com preço "4.99"
#    And vejo na página "generate_list" que os seguintes produtos "Vassoura", "Mortadela" e "Queijo" estão em falta no estoque
#    And estou na página "newListByStore"
#      When seleciono a loja "Mercadinho" na lista de lojas
#      And seleciono a opção "baixar"
#        Then o arquivo "ListaLoja.pdf" é enviado
#        And vejo uma lista com os itens "Vassoura" "3.4", "Mortadela" "2.45" e "Queijo" "5.5"
#        And "Vassoura" aparece na seção "Limpeza"
#        And "Mortadela" aparece na seção "Frios"
#        And "Queijo" aparece na seção "Frios"
#        And vejo que a seção "Frios" aparece antes de "Limpeza"
#        And no final do arquivo aparece o total de "11.35"
#
#  #Cenario 4:
#  Scenario: Cria lista de loja que não possui itens em falta pela GUI
#    Given a loja "Mercadinho" está registrada no sistema
#    And observo na página "generate_list" que não há itens em falta
#    And estou na página "newListByStore"
#      When seleciono a loja "Mercadinho" na lista de lojas
#      And seleciono a opção "baixar"
#        Then vejo uma mensagem informando "Lista não foi criada. Não existem itens em falta para essa loja"


  #Cenario 5:
  Scenario: Criar lista lista de loja quando não há lojas cadastradas

  #Cenario 6:


  #Cenario 7:


  #Cenario 8:

