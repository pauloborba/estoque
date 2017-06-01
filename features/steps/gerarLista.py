import string
import os
from PyPDF2 import PdfFileReader
from behave import given, when, then
from manager.models import Item, Store, Category, Price
from django.urls import reverse
from time import sleep


page_mapping = {'gerar lista de lojas': 'generate_list',\
				'principal': 'home'}


def getPort(url): #Retorna a porta da URL
    return url.split(':')[2].split('/')[0]

def create_item(item_name, qtd, min_qtd):
    Item.objects.create(item_name=item_name, qty=qtd, min_qty=min_qtd)

def create_store(store_name):	
    Store.objects.create(store_name=store_name)

def create_category(category_name, store_name):
	store = Store.objects.get(store_name=store_name)
	Category.objects.create(category_name=category_name, category_store=store)


def create_price(store, category, item, cost):
	store = Store.objects.get(store_name=store)
	category = Category.objects.get(category_name=category, category_store = store)
	item = Item.objects.get(item_name=item)
	Price.objects.create(cost_product=cost, price_category=category, price_product=item)




@given(u'Os produtos {prod1}, {prod2} estao cadastrados no sistema com quantidade {qtd} e quantidade minima {min_qtd}')
def step_impl(context, prod1, prod2, qtd, min_qtd):
    context.port = getPort(context.base_url)
    create_item(prod1, qtd, min_qtd)
    create_item(prod2, qtd, min_qtd)
    assert len(Item.objects.all()) >= 2

@given(u'A loja {store} esta cadastrada')
def step_impl(context, store):
    create_store(store)
    assert Store.objects.get(store_name=store) != None

@given(u'A loja {store} possui a sessao {category}')
def step_impl(context, store, category):
	create_category(category, store)
	store = Store.objects.get(store_name=store)
	assert Category.objects.get(category_name=category, category_store=store) != None

@given(u'A loja {store} possui {item1} na sessao {category1} com o preco {cost1} e {item2} na sessao {category2} com o preco {cost2}')
def step_impl(context, store, item1, category1, cost1, item2, category2, cost2):
    create_price(store, category1, item1, cost1)
    create_price(store, category2, item2, cost2)
    assert len(Price.objects.all()) >= 2

@given(u'So ha esses {qtd} itens cadastrados')
def step_impl(context, qtd):
	assert len(Item.objects.all()) == int(qtd)

@when('Eu navego para a pagina {page}')
def step_impl(context, page):
	page_url = page_mapping[page]
	context.browser.visit('http://localhost:'+context.port+reverse(page_url))
	assert context.browser.url == ('http://localhost:'+context.port+reverse(page_url))

@when('Eu desmarco a loja {store}')
def step_impl(context, store):
	context.browser.find_by_text(store).click()

@when(u'Eu seleciono a opcao gerar lista')
def step_impl(context):
	context.browser.find_by_id('generateList').click()
	sleep(5) # Esperar o download terminar para continuar
	# O certo seria fazer um callback mas não sei fazer isso em python ainda e não há tempo

@then(u'Eu recebo um arquivo e vejo escrito {store1} e vejo {item1} e vejo {item2} e nao vejo {store2}')
def step_impl(context, store1, item1, item2, store2):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	pdf = PdfFileReader(os.getcwd()+'/lista.pdf')
	pdf_content = pdf.getPage(0).extractText()
	assert store1 in pdf_content and item1 in pdf_content and item2 in pdf_content
	assert not store2 in pdf_content
	if os.path.isfile(os.getcwd()+'/lista.pdf'): #Remove o arquivo para os proximos passos
		os.remove(os.getcwd()+'/lista.pdf')


@then(u'Eu recebo um arquivo e vejo escrito Total {store} {total_cost}')
def step_impl(context, store, total_cost):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	pdf = PdfFileReader(os.getcwd()+'/lista.pdf')
	pdf_content = pdf.getPage(0).extractText()
	total_string = 'Total ' + store + ' - R$ ' + total_cost
	assert total_string in pdf_content
	if os.path.isfile(os.getcwd()+'/lista.pdf'): #Remove o arquivo para os proximos passos
		os.remove(os.getcwd()+'/lista.pdf')

@then(u'A quantidade do item {item} se mantem {qtd}')
def step_impl(context, item, qtd):
	item = Item.objects.get(item_name=item)
	assert int(item.qty) == int(qtd)

@then(u'O preco do item {item} na loja {store} se mantem {cost}')
def step_impl(context, item, store, cost):
	item = Item.objects.get(item_name=item)
	store = Store.objects.get(store_name=store)
	category = store.category_set.filter()
	prices = Price.objects.filter(price_product=item)
	for price in prices:
		if(price.price_category.category_store==store):
			new_cost = price.cost_product
			break
	assert float(new_cost) == float(cost)