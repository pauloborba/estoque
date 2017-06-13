# coding=utf-8
from behave import *
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from manager.models import Item, Category, Store, Price
from django.urls import reverse
from django.test import Client, TestCase
import string
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import os
from PyPDF2 import PdfFileReader
from time import sleep


# Controlador Cenario 1

@given('a loja "{loja}" está registrada no sistema')
def registra_loja(context, loja):
    delete_all_instaces()
    create_store(loja)
    loja_created = get_store_by_name(loja)
    assert loja_created is not None
    assert loja_created.store_name == loja


@given('as seções "{secao1}" e "{secao2}" foram cadastradas em "{loja}"')
def registra_duas_secoes(context, secao1, secao2, loja):
    registra_secao_and_check(context, secao1, loja)
    registra_secao_and_check(context, secao2, loja)


@given('os produtos "{item1}" e "{item2}" estão cadastrados no estoque')
def registra_dois_itens(context, item1, item2):
    registra_item_and_check(context, item1, 5, 5)
    registra_item_and_check(context, item2, 5, 5)


@given('os produtos "{item1}" e "{item2}" estão em falta no estoque')
def marca_dois_itens_em_falta(context, item1, item2):
    update_item_and_check(unicode(item1), 0, 5)
    update_item_and_check(unicode(item2), 0, 5)


@given('o produto "{item}" está em falta no estoque')
def marca_item_em_falta(context, item):
    update_item(item, 0, 5)
    item_created = get_item_by_name(item)
    assert item_created.qty < item_created.min_qty


@given('para a seção "{cat}" em "{store}" foi associado o produto "{item}" com preço "{price}"')
def cria_preco(context, cat, store, item, price):
    registra_preco_and_check(context, cat, store, item, price)


@when('eu solicito a criação da lista exclusiva para "{store}"')
def solicita_criacao_de_lista_para_loja(context, store):
    go_pag_new_list_by_store(context)
    seleciona_store(context, store)
    baixa_store(context,"baixar")
    sleep(3)


@then('o arquivo "{file_name}" é enviado')
def check_arquivo(context, file_name):
    pdf = PdfFileReader(os.getcwd() + '/' + file_name)
    context.pdf_content = pdf.getPage(0).extractText()
    assert context.pdf_content is not None


@then('vejo no arquivo que a seção "{category}" não aparece')
def step_impl(context, category):
    assert not(category in context.pdf_content)


@then('a seção "{cat}" aparece com os itens "{item1}" "{price1}" e "{item2}" "{price2}"')
def step_impl(context, cat, item1, price1, item2, price2):
    assert cat in context.pdf_content
    assert item1 in context.pdf_content
    assert price1 in context.pdf_content
    assert item2 in context.pdf_content
    assert price2 in context.pdf_content


@then('no final do arquivo aparece o total de "{price_tot}"')
def step_impl(context, price_tot):
    assert price_tot in context.pdf_content
    clean_files()


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
    assert not os.path.isfile(os.getcwd() + '/' + file_name)


# GUI Cenario 1

@given('a loja "{store}" tem 3 seções cadastradas: "{cat1}", "{cat2}" e "{cat3}", nessa ordem')
def step_impl(context, store, cat1, cat2, cat3):
    registra_secao_and_check(context, cat1, store)
    registra_secao_and_check(context, cat2, store)
    registra_secao_and_check(context, cat3, store)


@given('para a seção "{cat}" em "{store}" foram associados os seguintes produtos: "{item1}" com preço "{price1}" e "{item2}" com preço "{price2}"')
def step_cria_dois_precos(context, cat, store, item1, price1, item2, price2):
    registra_preco_and_check(context, cat, store, item1, price1)
    registra_preco_and_check(context, cat, store, item2, price2)


@given('vejo na página "generate_list" que os seguintes produtos "{item1}", "{item2}" e "{item3}" estão em falta no estoque')
def step_impl(context, item1, item2, item3):
    go_generate_list(context)
    assert str(context.browser.url).endswith('/generate_list/')
    linesItems = context.browser.find_by_css('.red-text')
    assert linesItems is not None
    items = []
    for i in linesItems:
        items.append(i.text.split(' ', 1)[0])
    assert item1 in items
    assert item2 in items
    assert item3 in items
    sleep(2)


@then('vejo uma lista com os itens "{item1}" "{price1}", "{item2}" "{price2}" e "{item3}" "{price3}"')
def step_impl(context, item1, price1, item2, price2, item3, price3):
    assert item1 in context.pdf_content
    assert price1 in context.pdf_content
    assert item2 in context.pdf_content
    assert price2 in context.pdf_content
    assert item3 in context.pdf_content
    assert price3 in context.pdf_content


@then('"{item1}" aparece na seção "{category}"')
def step_impl(context, item1, category):
    assert category in context.pdf_content
    assert context.pdf_content.find(category) < context.pdf_content.find(item1)


@then('vejo que a seção "{cat1}" aparece antes de "{cat2}"')
def step_impl(context, cat1, cat2):
    assert context.pdf_content.find(cat1) < context.pdf_content.find(cat2)


# GUI Cenario 2


@given('observo na página "generate_list" que não há itens em falta')
def go_pag_generate_list(context):
    # abre a pagina inicial
    open_home(context)
    # Seleciona no menu e vai para /generate_list/
    context.browser.find_by_id('linkGenerateList').click()
    sleep(3)
    assert str(context.browser.url).endswith('/generate_list/')
    # Veriificar se não há objetos marcados em vermelho, ou seja, item em falta
    assert context.browser.is_element_not_present_by_css('.red-text')


@when('navego para a página "newListByStore"')
def go_pag_new_list_by_store(context):
    open_home(context)
    # Seleciona no menu e vai para /newListByStore/
    context.browser.find_by_id('linkListByStore').click()
    sleep(3)
    assert str(context.browser.url).endswith("/newListByStore/")


@when('seleciono a loja "{store}" na lista de lojas')
def seleciona_store(context, store):
    select_store = get_store_by_name(store)
    # Seleciona input type:radio por 'name' e 'value'
    context.browser.choose('store', select_store.id)
    sleep(1)


@when('seleciono a opção "{opcao}"')
def baixa_store(context, opcao):
    if opcao == "cancelar":
        btn = context.browser.find_by_name('btn-cancel').first  # context.browser.find_by_name('action').first
        btn.click()
    elif opcao == "baixar":
        btn = context.browser.find_by_name('btn-submit').first  # context.browser.find_by_name('action').first
        btn.click()
    sleep(3)


@then('vejo uma mensagem informando "{message}"')
def step_impl(context, message):
    assert context.browser.is_text_present(message)
    clean_files()


@given("não existe lojas registradas no sistema")
def nao_ha_lojas(context):
    delete_all_stores()


@then("não vejo opções para solicitar a criação de lista")
def step_impl(context):
    assert context.browser.is_text_not_present("Baixar")


@given('vejo na página "generate_list" que os produtos "{item1}" e "{item2}" estão em falta no estoque')
def step_impl(context, item1, item2):
    go_generate_list(context)
    assert str(context.browser.url).endswith('/generate_list/')
    linesItems = context.browser.find_by_css('.red-text')
    assert linesItems is not None
    items = []
    for i in linesItems:
        items.append(i.text.split(' ', 2)[0] + " " + i.text.split(' ', 2)[1])
    assert item1 in items
    assert item2 in items
    sleep(2)


@then('a página é encaminhada para "home"')
def step_impl(context):
    assert str(context.browser.url).endswith("/home/")


@then('no arquivo aparece "{store}" como nome da loja')
def verifica_store_name_no_arquivo(context, store):
    assert store in context.pdf_content


@given('a seção "{category}" foi cadastrada em "{store}"')
def registra_categoria_em_loja(context, category, store):
    registra_secao_and_check(context, category, store)


@given('o produto "{item}" foi cadastrado no estoque com quantidade "{qtd}" e quantidade mínima "{min_qtd}"')
def registra_item(context, item, qtd, min_qtd):
    registra_item_and_check(context, item, float(qtd), float(min_qtd))


@then('a quantidade do item "{item}" permanace "{qtd}"')
def step_impl(context, item, qtd):
    item_instace = get_item_by_name(item)
    assert item_instace is not None
    assert item_instace.qty == int(qtd)


@then('a quantidade mínima do produto "{item}" permanece "{qtd_min}"')
def step_impl(context, item, qtd_min):
    item_instace = get_item_by_name(item)
    assert item_instace is not None
    assert item_instace.min_qty == int(qtd_min)


@then('na seção "{cat}" em "{store}" o preço do produto "{item}" permanece "{price}"')
def step_impl(context, cat, store, item, price):
    assert get_price(price,cat,store,item).cost_product == float(price)


# Funções auxiliares

def get_store_by_name(store):
    instace_loja = Store.objects.get(store_name=store)
    return instace_loja


def create_store(store):
    Store.objects.create(store_name=store)


def create_category(category, store):
    Category.objects.create(category_name=category, category_store=get_store_by_name(store))


def get_category_by_name(category, store):
    instace_store = get_store_by_name(store)
    instace_category = instace_store.category_set.filter(category_name=category)
    return instace_category[0]


def get_item_by_name(item):
    instace_item = Item.objects.get(item_name=item)
    return instace_item


def create_item(item, quant, min_quant):
    Item.objects.create(item_name=item, qty=quant, min_qty=min_quant)


def update_item(item, quant, min_quant):
    instace_item = get_item_by_name(item)
    instace_item.qty = quant
    instace_item.min_qty = min_quant
    instace_item.save()


def update_item_and_check(name, quant, min_quant):
    update_item(name, quant, min_quant)
    item_created = get_item_by_name(name)
    assert item_created.qty < item_created.min_qty


def create_price(price, category, store, item):
    Price.objects.create(
        cost_product=float(price),
        price_category=get_category_by_name(category, store),
        price_product=get_item_by_name(item)
    )


def get_price(price, category, store, item):
    instace_price = Price.objects.get(
        cost_product=float(price),
        price_category=get_category_by_name(category, store),
        price_product=get_item_by_name(item)
    )
    return instace_price


def open_home(context):
    context.browser.visit(context.base_url + '/home/')
    sleep(2) # aguarda reencamiar para home
    assert str(context.browser.url).endswith("/home/")


def gui_create_price(context, price, cat, store, item):
    context.browser.find_by_id('criarPreco').click()
    price_val = context.browser.find_by_id("priceInput")
    price_val.fill(price)
    select_item = get_item_by_name(item)
    context.browser.choose('item', select_item.id)
    select_cat = get_category_by_name(cat, store)
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
    select_store = get_store_by_name(store)
    context.browser.find_by_id('new_category').click()
    name = context.browser.find_by_id("categoryNameInput")
    name.fill(cat)
    context.browser.choose('store', select_store.id)
    context.browser.find_by_tag('button').first.click()


def registra_secao_and_check(context, secao, loja):
    create_category(secao, loja)
    category_created = get_category_by_name(secao, loja)
    assert category_created is not None
    assert category_created.category_name == secao


def registra_item_and_check(context, item, quant, quant_min):
    item = unicode(item)
    create_item(item, quant, quant_min)
    item_created_1 = get_item_by_name(item)
    assert item_created_1 is not None
    assert item_created_1.item_name == item


def registra_preco_and_check(context, cat, store, item, price):
    create_price(price, cat, store, item)
    price_created = get_price(price, cat, store, item)
    assert price_created is not None
    assert price_created.cost_product == float(price)


def delete_all_stores():
    Store.objects.all().delete()


def delete_all_items():
    Item.objects.all().delete()


def delete_all_instaces():
    delete_all_stores()
    delete_all_items()


def clean_files():
    if os.path.isfile(os.getcwd() + '/ListaLoja.pdf'):  # Remove o arquivo para os proximos passos
        os.remove(os.getcwd() + '/ListaLoja.pdf')


def go_generate_list(context):
    open_home(context)
    # Seleciona no menu e vai para /generate_list/
    context.browser.find_by_id('linkGenerateList').click()
    sleep(2)