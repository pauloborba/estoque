import string
from behave import *
from django.http import  *
from django.contrib import messages

#cadastrar valor para item que nao esta disponivel na loja escolhido

@given('eu estou na pagina de cadastramento de precos')
def new_price(context):
    br = context.browser
    br.visit(context.base_url+'/newPrice/')

@given('eu vejo o item "{item}" na lista de itens cadastrados')
def see_item(context, item):
    br = context.browser
    response = br.status_code
    assert response.code == 200
    assert br.url.endswith("/newPrice/")













'''
#  Scenario: Cadastrar valor para item que não está disponível na loja escolhido - GUI
@given('Eu estou na pagina de cadastramento de precos')
def step_impl(context):
	br = context.browser
	br.visit(context.new_price)
	response = br.status_code
	assert response.code == 200
	assert br.url.endswith("/newPrice/")

def create_item(context, item_name, enough):
    context.browser.get(reverse('new_item'))
    form = context.browser.get(context.browser, tag = 'form')
    get_element(form, id="item_name").send_keys(item_name, enough)
    form.submit

@given('eu vejo o item "{it}" na lista de itens cadastrados')
def step_impl(context, it):
	br = context.browser
	create_item(context, it, True)
	itemList = br.find_by_id('itemList')
	assert itemList.get(name = it) != None

@given('eu vejo a loja "{it}" na lista de lojas cadastradas')
def step_impl(context, it):
	br = context.browser
	new_store()
	storeList = br.find_by_id('storeList')
	assert storeList.get(name = it) != None

@given('a loja "{loja}" nao possui o item "{item}"')
def step_impl(context, loja, item):
	br = context.browser
	itemList = br.find_by_id('itemList')
	storeList = br.find_by_id('storeList')
	it = itemList.get(name = item)
	st = storeList.get(name = loja)
	assert (Controller.verifyIteminStore(it, st))

@when('eu tento cadastrar o preco "{preco}" para o item "{item}" na loja "{loja}"')
def step_impl(context, preco, item):
	br = context.browser
	itemList = br.find_by_id('itemList')
	storeList = br.find_by_id('storeList')
	editText = br.find_by_id('editText')
	it = itemList.get(name = item)
	st = storeList.get(name = loja)
	it.select()
	st.select()
	editText.fill(preco)
	button = br.find_by_id('createPrice')
	button.click()

@then('eu vejo uma mensagem informando que a loja "{loja}" nao possui o item "{item}"')
def step_impl(context):
	Controller.showException(["pt-br", "A loja "+loja+" não possui o item "+item])

@then('eu permaneco na pagina de cadastramento de precos')
def step_impl(context):
	br = context.browser
	response = br.status_code
	assert response.code == 200
	assert br.url.endswith("/newPrice/")
'''