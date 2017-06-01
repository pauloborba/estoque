# coding=utf-8
from behave import *
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from manager.models import Item, Category, Store, Price
from sets import Set
from django.urls import reverse
from django.test import Client, TestCase
import string
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest


# Controlador Cenario 1

@given('a loja "{loja}" está registrada no sistema')
def registra_loja(context, loja):
    createStore(loja)
    loja_created = getStoreByName(loja)
    assert loja_created is not None


@given('as seções "{secao1}" e "{secao2}" foram cadastradas em "{loja}"')
def registra_duas_secoes(context, secao1, secao2, loja):
    create_category(secao1, loja)
    create_category(secao2, loja)
    category_created_1 = getCategoryByName(secao1, loja)
    category_created_2 = getCategoryByName(secao2, loja)
    assert category_created_1 is not None
    assert category_created_2 is not None


@given('os produtos "{item1}" e "{item2}" estão cadastrados no estoque')
def registra_dois_itens(context, item1, item2):
    create_item(item1, 5, 5)
    item_created_1 = getItemByName(item1)
    create_item(item2, 5, 5)
    item_created_2 = getItemByName(item2)
    assert item_created_1 is not None
    assert item_created_2 is not None


@given('os produtos "{item1}" e "{item2}" estão em falta no estoque')
def marca_dois_itens_em_falta(context, item1, item2):
    updateItemQty(item1, 0, 5)
    updateItemQty(item2, 0, 5)

@given('o produto "{item}" está associado com a seção "{secao}" de "{loja}" com preço de R$ "{preco}"')
def associa_dois_itens_com_secao(context, item, secao, loja, preco):
    create_price(preco, secao, loja, item)
    price_created = getPrice(preco, secao, loja, item)
    assert price_created is not None


@when('eu solicito a criação da lista exclusiva para "{loja}"')
def solicita_criacao_de_lista_para_loja(context, loja):
    c = Client()
    response = c.post('/newListByStore/', {'store': loja})
    context.response = response


@then('o arquivo "{file_name}" é enviado')
def check_arquivo(context, file_name):
    assert str(context.response.get('Content-Disposition')).find(file_name) == -1


# Controlador Cenario 2

@given('existem no sistema "0" produtos em falta')
def existem_zero_produtos_em_falta(context):
    create_item("arroz", 5, 5)
    create_item("Fuba", 10, 2)
    create_item("Pão", 6, 4)
    items = Item.objects.all()
    missingItem = False
    for item in items:
        if item.qty < item.min_qty:
            missingItem = True
    assert not missingItem


@then('o arquivo "{file_name}" não é enviado')
def check_not_arquivo(context, file_name):
    assert context.response.get('Content-Disposition') is None


# GUI Cenario 1


server_name = "http://localhost:8000"


@given('a loja "{store}" foi registrada no sistema')
def step_impl(context, store):
    sigin(context)
    context.browser.find_by_id('new_store').click()
    name = context.browser.find_by_id("storeNameInput")
    name.fill(store)
    context.browser.find_by_tag('button').first.click()


@given('a loja "{store}" tem 3 seções cadastradas: "{cat1}", "{cat2}" e "{cat3}", nessa ordem')
def step_impl(context, store, cat1, cat2, cat3):
    gui_create_category(context, cat1, store)
    gui_create_category(context, cat2, store)
    gui_create_category(context, cat3, store)


@given('os produtos "{item1}", "{item2}", "{item3}" e "{item4}" foram cadastrados')
def step_impl(context, item1, item2, item3, item4):
    gui_create_item(context, item1, 6, 5)
    gui_create_item(context, item2, 3, 5)
    gui_create_item(context, item3, 3, 5)
    gui_create_item(context, item4, 3, 5)


@given('para a seção "{cat}" em "{store}" foi associado o produto "{item}" com preço "{price}"')
def step_impl(context, price, cat, store, item):
    gui_create_price(context, price, cat, store, item)


@given('para a seção "{cat}" em "{store}" foram associados os seguintes produtos: "{item1}" com preço "{price1}" e "{item2}" com preço "{price2}"')
def step_impl(context, price1, price2, cat, store, item1, item2):
    gui_create_price(context, price1, cat, store, item1)
    gui_create_price(context, price2, cat, store, item2)


@given('vejo na página "generate_list" que os seguintes produtos "{item1}", "{item2}" e "{item3}" estão em falta no estoque')
def step_impl(context, item1, item2, item3):
    # Seleciona no menu e vai para /generate_list/
    context.browser.find_by_id('linkGenerateList').click()
    items = context.browser.find_by_css('.red-text')
    assert items is not None
    assert verify_item_in_set(item1,items)
    assert verify_item_in_set(item2,items)
    assert verify_item_in_set(item3,items)


@then('vejo que um arquivo pdf de nome "{file_name}" foi baixado')
def step_impl(context,file_name):
    assert str(context.response.get('Content-Disposition')).find(file_name) == -1


# GUI Cenario 2


@given('observo na página "generate_list" que não há itens em falta')
def go_pag_generate_list(context):
    # abre a pagina inicial e loga
    sigin(context)
    # Seleciona no menu e vai para /generate_list/
    context.browser.find_by_id('linkGenerateList').click()
    # Veriificar se não há objetos marcados em vermelho, ou seja, item em falta
    assert context.browser.is_element_not_present_by_css('.red-text')


@given('estou na página "newListByStore"')
def go_pag_new_list_by_store(context):
    # Volta para a pagina /home/
    context.browser.back()
    # Seleciona no menu e vai para /newListByStore/
    context.browser.find_by_id('linkListByStore').click()
    assert context.browser.status_code.is_success()


@when('seleciono a loja "{store}" na lista de lojas')
def step_impl(context, store):
    select_store = getStoreByName(store)
    # Seleciona input type:radio por 'name' e 'value'
    context.browser.choose('store', select_store.id)


@when('seleciono a opção "baixar"')
def step_impl(context):
    btn = context.browser.find_by_name('btn-submit').first  # context.browser.find_by_name('action').first
    btn.click()


@then('vejo uma mensagem informando "{message}"')
def step_impl(context, message):
    assert context.browser.is_text_present(message)


# Funções auxiliares

def getStoreByName(store):
    instace_loja = Store.objects.get(store_name=store)
    return instace_loja


def createStore(store):
    Store.objects.create(store_name=store)


def create_category(category, store):
    Category.objects.create(category_name=category, category_store=getStoreByName(store))


def getCategoryByName(category, store):
    instace_store = getStoreByName(store)
    instace_category = instace_store.category_set.filter(category_name=category)
    return instace_category[0]


def getItemByName(item):
    instace_item = Item.objects.get(item_name=item)
    return instace_item


def create_item(item, quant, min_quant):
    Item.objects.create(item_name=item, qty=quant, min_qty=min_quant)


def updateItemQty(item, quant, min_quant):
    instace_item = getItemByName(item)
    instace_item.qty = quant
    instace_item.min_qty = min_quant


def create_price(price, category, store, item):
    Price.objects.create(
        cost_product=float(price),
        price_category=getCategoryByName(category, store),
        price_product=getItemByName(item)
    )


def getPrice(price, category, store, item):
    instace_price = Price.objects.get(
        cost_product=float(price),
        price_category=getCategoryByName(category, store),
        price_product=getItemByName(item)
    )
    return instace_price


def sigin(context):
    # antes do teste rode via comand line
    # python manage.py createsuperuser
    # Username: test
    # Email address: test@mail.com
    # Password: adminadm
    # Password(again): adminadm
    # por fim, certifique-se de ver a mensagem: "Superuser created successfully."
    context.browser.visit(server_name + '/')
    user = context.browser.find_by_id("usernameInput")
    user.fill('test')
    pwd = context.browser.find_by_id("pwdInput")
    pwd.fill('adminadm')
    # Autentica e vai para /Home/
    context.browser.find_by_tag('button').first.click()


def verify_item_in_set(item,items):
    values = []
    for i in items:
        values.append(i.text)
    return item in values


def gui_create_price(context, price, cat, store, item):
    context.browser.find_by_id('new_price').click()
    price_val = context.browser.find_by_id("priceInput")
    price_val.fill(price)
    select_item = getItemByName(item)
    context.browser.choose('item', select_item.id)
    select_cat = getCategoryByName(cat, store)
    context.browser.choose('category', select_cat.id)
    # Cadastra e vai para /Home/
    context.browser.find_by_tag('button').first.click()


def gui_create_item(context, item, qty, min):
    context.browser.find_by_id('new_item').click()
    name = context.browser.find_by_id("itemNameInput")
    name.fill(item)
    quant = context.browser.find_by_id("itemQtyInput")
    quant.fill(qty)
    min_quant = context.browser.find_by_id("itemMinQtyInput")
    min_quant.fill(min)
    context.browser.find_by_tag('button').first.click()


def gui_create_category(context, cat, store):
    select_store = getStoreByName(store)
    context.browser.find_by_id('new_category').click()
    name = context.browser.find_by_id("categoryNameInput")
    name.fill(cat)
    context.browser.choose('store', select_store.id)
    context.browser.find_by_tag('button').first.click()
