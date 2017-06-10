# coding=utf-8
from behave import *
from manager.models import *
from sets import Set
# from django.urls import reverse
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
import string
import requests
from manager import views
from django.test.client import RequestFactory
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest


# Controlador Cenario 1

@given(u'a loja "{loja}" esta cadastrada no sistema')
def cadastrar_loja(context, loja):
    views.create_new_store(None, loja)
    assert Store.objects.get(store_name=loja) != None


@given(u'a secao "{secao}" esta cadastrada no sistema para a loja "{loja}"')  # seria interessante criar a loja aqui?
def cadastrar_secao(context, secao, loja):
    lojaObject = Store.objects.get(store_name=loja)
    views.create_new_category(None, secao, lojaObject)
    assert Category.objects.get(category_name=secao, category_store=lojaObject) != None


@given(u'o preço "{preco}" esta cadastrado no sistema para o produto "{item}" na secao "{secao}" da loja "{loja}"')
def cadastrar_item_com_secao(context, preco, item, secao, loja):
    views.create_new_item(None, item_name=item, qty=float(10), min_qty=float(0))
    itemObject = Item.objects.get(item_name=item)
    assert itemObject != None
    views.create_new_store(None, loja)
    lojaObject = Store.objects.get(store_name=loja)
    assert lojaObject != None
    views.create_new_category(None, secao, lojaObject)
    secaoObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    assert secaoObject != None
    views.create_new_price(None, preco, secaoObject, itemObject)
    precoObject = Price.objects.get(cost_product=float(preco), price_category=secaoObject, price_product=itemObject)
    assert precoObject != None

@given(u'o produto "{item}" esta cadastrado no sistema')
def cadastrar_produto(context, item):
    views.create_new_item(None, item_name=item, qty=10, min_qty=10)
    assert Item.objects.get(item_name=item) != None


@given(u'nao existe preco cadastrado para o produto "{item}" na secao "{secao}" da loja "{loja}"')
def verificar_preco_nao_existente(context, item, secao, loja):
    secaoObject = Category.objects.get(category_name=secao, category_store__store_name=loja)
    assert secaoObject != None
    itemObject = Item.objects.get(item_name=item)
    assert itemObject != None
    assert (Price.objects.filter(price_product=itemObject, price_category=secaoObject).count() == 0)


@given(u'nao existe outros precos cadastrados alem dos precos para os items "{item1}" e "{item2}"')
def verificar_outros_precos(context, item1, item2):
    assert Price.objects.filter(price_product__item_name=item1).count() == 1
    assert Price.objects.filter(price_product__item_name=item2).count() == 1
    assert Price.objects.all().count() == 2


@when(u'eu tento cadastrar o preco "{preco}" do produto "{item}" na secao "{secao}" da loja "{loja}"')
def tentar_cadastrar_preco(context, preco, item, secao, loja):
    itemObject = Item.objects.get(item_name=item)
    assert itemObject != None
    lojaObject = Store.objects.get(store_name=loja)
    secaoObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    assert secaoObject != None
    views.create_new_price(None, preco, secaoObject, itemObject)
    assert Price.objects.get(cost_product=preco, price_category=secaoObject, price_product=itemObject)


@then(u'o sistema verifica que o preco para o produto "{item}" na secao "{secao}" da loja "{loja}" e o que possui mais historicos')
def verificar_mais_historico(context, item, secao, loja):
    i = 0
    itemObject = Item.objects.get(item_name=item)
    lojaObject = Store.objects.get(store_name=loja)
    secaoObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    priceObject = Price.objects.get(price_product=itemObject, price_category=secaoObject)
    priceAux = None
    for p in Price.objects.all():
        if(p.history_set.count()>i):
            i = p.history_set.count()
            priceAux = p
    assert priceAux == priceObject

@when(u'eu sobrescrevo o preco para o produto "{item}" na secao "{secao}" da loja "{loja}" para "{preco}"')
def sobrescrevo_preco(context, item, secao, loja, preco):
    itemObject = Item.objects.get(item_name=item)
    lojaObject = Store.objects.get(store_name=loja)
    secaoObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    precoObject = Price.objects.get(price_product=itemObject, price_category=secaoObject)
    views.create_new_price(None, preco, secaoObject, itemObject)
    assert Price.objects.get(cost_product=preco, price_category=secaoObject, price_product=itemObject)

@then(u'o sistema cadastra corretamente o preco "{preco}" para o produto "{item}" na secao "{secao}" da loja "{loja}"')
def cadastrar_preco_nao_existente(context, preco, item, secao, loja):
    itemObject = Item.objects.get(item_name=item)
    assert itemObject != None
    secaoObject = Category.objects.get(category_name=secao, category_store__store_name=loja)
    assert secaoObject != None
    views.create_new_price(None, preco, secaoObject, itemObject)
    precoObject = Price.objects.get(cost_product=preco, price_product=itemObject, price_category=secaoObject)
    assert precoObject != None
    assert (float(precoObject.cost_product) == float(preco))

@then(u'e criado um historico de precos para o produto "{item}" na secao "{secao}" da loja "{loja}"')
def criar_historico_para_um_produto(context, item, secao, loja):
    itemObject = Item.objects.get(item_name=item)
    storeObject = Store.objects.get(store_name=loja)
    categoryObject = Category.objects.get(category_name=secao, category_store=storeObject)
    preco = Price.objects.get(price_product=itemObject, price_category=categoryObject)
    assert preco.history_set.all().count() >0

@then(u'o sistema sobrescreve o preco do produto "{item}" na loja "{loja}" para o valor "{preco}"')
def sobrescrever_preco(context, item, loja, preco):
    itemObject = Item.objects.get(item_name=item)
    assert item != None
    lojaObject = Store.objects.get(store_name=loja)
    assert lojaObject != None
    # secaoObject = Category.objects.get(category_store=lojaObject)
    # assert  secaoObject != None
    priceObject = Price.objects.get(cost_product=preco, price_product=itemObject,
                                    price_category__category_store=lojaObject)
    assert priceObject != None
    assert (priceObject.cost_product) == float(preco)
    assert (priceObject.price_product == itemObject)
    assert (priceObject.price_category.category_store == lojaObject)


