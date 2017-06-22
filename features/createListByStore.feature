Feature: Gerar lista de compras de uma determinada loja que possui seções      


  #Cenario 1 (Controlador):
  Scenario: Cria lista de loja
    Given a loja "Mercadinho" está registrada no sistema
    And as seções "Bebidas" e "Frios" foram cadastradas em "Mercadinho"
    And os produtos "Mortadela" e "Queijo Coalho" estão cadastrados no estoque
    And os produtos "Mortadela" e "Queijo Coalho" estão em falta no estoque
    And para a seção "Frios" em "Mercadinho" foi associado o produto "Mortadela" com preço "2.45"
    And para a seção "Frios" em "Mercadinho" foi associado o produto "Queijo Coalho" com preço "5.5"
      When eu solicito a criação da lista exclusiva para "Mercadinho"
        Then o arquivo "ListaLoja.pdf" é enviado
        And a seção "Frios" aparece com os itens "Queijo Coalho" "5.5" e "Mortadela" "2.45"
        And no final do arquivo aparece o total de "7.95"


  #Cenario 2 (Controlador):
  Scenario: Cria lista de loja que não possui itens em falta
    Given a loja "Mercadinho" está registrada no sistema
    And existem no sistema "0" produtos em falta
      When eu solicito a criação da lista exclusiva para "Mercadinho"
        Then o arquivo "ListaLoja.pdf" não é enviado


  #Cenario 7 (Controlador):
  Scenario: Cria lista para uma loja com caracteres especiais(ç, á, etc) no nome
    Given a loja "Pão de Açúcar" está registrada no sistema
    And as seções "Bomboniere" e "Massas" foram cadastradas em "Pão de Açúcar"
    And os produtos "1kg Pão Francês" e "Chocolate Branco" estão cadastrados no estoque
    And os produtos "1kg Pão Francês" e "Chocolate Branco" estão em falta no estoque
    And para a seção "Bomboniere" em "Pão de Açúcar" foi associado o produto "Chocolate Branco" com preço "8.73"
    And para a seção "Massas" em "Pão de Açúcar" foi associado o produto "1kg Pão Francês" com preço "6.99"
      When eu solicito a criação da lista exclusiva para "Pão de Açúcar"
        Then o arquivo "ListaLoja.pdf" é enviado
        And no arquivo aparece "Pão de Açúcar" como nome da loja
        And "1kg Pão Francês" aparece na seção "Massas"
        And "Chocolate Branco" aparece na seção "Bomboniere"
        And no final do arquivo aparece o total de "15.72"


  #Cenario 8 (Controlador):
  Scenario: Criar lista de uma loja não altera o preço e a quantidade dos itens associados a loja
    Given a loja "Hiper Bompreço" está registrada no sistema
    And a seção "Eletrodomésticos" foi cadastrada em "Hiper Bompreço"
    And o produto "Ventilador" foi cadastrado no estoque com quantidade "1" e quantidade mínima "2"
    And o produto "Fogão" foi cadastrado no estoque com quantidade "0" e quantidade mínima "1"
    And para a seção "Eletrodomésticos" em "Hiper Bompreço" foi associado o produto "Ventilador" com preço "129.99"
    And para a seção "Eletrodomésticos" em "Hiper Bompreço" foi associado o produto "Fogão" com preço "699"
      When eu solicito a criação da lista exclusiva para "Hiper Bompreço"
        Then o arquivo "ListaLoja.pdf" é enviado
        And a seção "Eletrodomésticos" aparece com os itens "Ventilador" "129.99" e "Fogão" "699"
        And no final do arquivo aparece o total de "828.99"
        And a quantidade do item "Ventilador" permanace "1"
        And a quantidade mínima do produto "Ventilador" permanece "2"
        And a quantidade do item "Fogão" permanace "0"
        And a quantidade mínima do produto "Fogão" permanece "1"
        And na seção "Eletrodomésticos" em "Hiper Bompreço" o preço do produto "Ventilador" permanece "129.99"
        And na seção "Eletrodomésticos" em "Hiper Bompreço" o preço do produto "Fogão" permanece "699"


  #Cenario 3 (GUI):
  Scenario: Cria lista de Loja que possui seções ordenadas
    Given a loja "Mercadinho" está registrada no sistema
    And a loja "Mercadinho" tem 3 seções cadastradas: "Cereais", "Frios" e "Limpeza", nessa ordem
    And os produtos "Aveia" e "Vassoura" estão cadastrados no estoque
    And os produtos "Mortadela" e "Queijo" estão cadastrados no estoque
    And os produtos "Mortadela" e "Queijo" estão em falta no estoque
    And o produto "Vassoura" está em falta no estoque
    And para a seção "Limpeza" em "Mercadinho" foi associado o produto "Vassoura" com preço "3.4"
    And para a seção "Frios" em "Mercadinho" foram associados os seguintes produtos: "Mortadela" com preço "2.45" e "Queijo" com preço "5.5"
    And para a seção "Cereais" em "Mercadinho" foi associado o produto "Aveia" com preço "4.99"
    And vejo na página "generate_list" que os seguintes produtos "Vassoura", "Mortadela" e "Queijo" estão em falta no estoque
      When navego para a página "newListByStore"
      And seleciono a loja "Mercadinho" na lista de lojas
      And seleciono a opção "baixar"
        Then o arquivo "ListaLoja.pdf" é enviado
        And vejo uma lista com os itens "Vassoura" "3.4", "Mortadela" "2.45" e "Queijo" "5.5"
        And "Vassoura" aparece na seção "Limpeza"
        And "Mortadela" aparece na seção "Frios"
        And "Queijo" aparece na seção "Frios"
        And vejo que a seção "Frios" aparece antes de "Limpeza"
        And no final do arquivo aparece o total de "11.35"


  #Cenario 4 (GUI):
  Scenario: Cria lista de loja que não possui itens em falta pela GUI
    Given a loja "Mercadinho" está registrada no sistema
    And observo na página "generate_list" que não há itens em falta
      When navego para a página "newListByStore"
      And seleciono a loja "Mercadinho" na lista de lojas
      And seleciono a opção "baixar"
        Then vejo uma mensagem informando "Lista não foi criada. Não existem itens em falta para essa loja"


  #Cenario 5 (GUI):
  Scenario: Criar lista de loja quando não há lojas cadastradas
    Given não existe lojas registradas no sistema
      When navego para a página "newListByStore"
        Then vejo uma mensagem informando "Nenhuma Loja registrada!"
        And vejo uma mensagem informando "Por favor registre alguma loja aqui."
        And não vejo opções para solicitar a criação de lista


  #Cenario 6 (GUI):
  Scenario: Cancelar criação de lista de loja
    Given a loja "Extra" está registrada no sistema
    And as seções "Bebidas" e "Carnes" foram cadastradas em "Extra"
    And os produtos "1L CocaCola" e "1/2Kg Fraldinha" estão cadastrados no estoque
    And os produtos "1L CocaCola" e "1/2Kg Fraldinha" estão em falta no estoque
    And para a seção "Bebidas" em "Extra" foi associado o produto "1L CocaCola" com preço "6.99"
    And para a seção "Carnes" em "Extra" foi associado o produto "1/2Kg Fraldinha" com preço "15.99"
    And vejo na página "generate_list" que os produtos "1L CocaCola" e "1/2Kg Fraldinha" estão em falta no estoque
    When navego para a página "newListByStore"
      And seleciono a loja "Extra" na lista de lojas
      And seleciono a opção "cancelar"
        Then o arquivo "ListaLoja.pdf" não é enviado
        And a página é encaminhada para "home"