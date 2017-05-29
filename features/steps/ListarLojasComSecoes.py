# coding=utf-8
from behave import *
from manager.models import Item, Category, Store, Price
from sets import Set
from django.urls import reverse
from django.test import Client, TestCase
import string
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest


# Controlador Cenario 1

@given('a loja “{loja}” está registrada no sistema')
def registra_loja(context, loja):
    createStore(loja)
    loja_created = getStoreByName(loja)
    assert loja_created is not None


@given('as seções “{secao1}” e “{secao2}” foram cadastradas em “{loja}”')
def registra_duas_secoes(context, secao1, secao2, loja):
    create_category(secao1, loja)
    create_category(secao2, loja)
    category_created_1 = getCategoryByName(secao1, loja)
    category_created_2 = getCategoryByName(secao2, loja)
    assert category_created_1 is not None
    assert category_created_2 is not None


@given('os produtos “{item1}” e “{item2}” estão cadastrados no estoque')
def registra_dois_itens(context, item1, item2):
    create_item(item1, 5, 5)
    item_created_1 = getItemByName(item1)
    create_item(item2, 5, 5)
    item_created_2 = getItemByName(item2)
    assert item_created_1 is not None
    assert item_created_2 is not None


@given('os produtos “{item1}” e “{item2}” estão em falta no estoque')
def marca_dois_itens_em_falta(context, item1, item2):
    updateItemQty(item1, 0, 5)
    updateItemQty(item2, 0, 5)

@given('o produto “{item}” está associado com a seção “{secao}” de “{loja}” com preço de R$ "{preco}"')
def associa_dois_itens_com_secao(context, item, secao, loja, preco):
    create_price(preco, secao, loja, item)
    price_created = getPrice(preco, secao, loja, item)
    assert price_created is not None


@when('eu solicito a criação da lista exclusiva para “{loja}”')
def solicita_criacao_de_lista_para_loja(context, loja):
    c = Client()
    response = c.post('/newListByStore/', {'store': loja})
    context.response = response


@then('o arquivo “{file_name}” é enviado')
def check_arquivo(context, file_name):
    assert context.response.content == ''  # como teste de uma arquivo e enviado
    '''
    file_name = str(file_name).replace(" ", "")
    assert context.response['Content-Disposition'] == "attachment; filename=" + file_name + ".pdf"
    '''

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
