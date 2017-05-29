# coding=utf-8
from behave import *
from manager.models import *
from sets import Set
#from django.urls import reverse
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

@given(u'a secao "{secao}" esta cadastrada no sistema para a loja "{loja}"') #seria interessante criar a loja aqui?
def cadastrar_secao(context, secao, loja):
    lojaObject = Store.objects.get(store_name=loja)
    views.create_new_category(None, secao, lojaObject)
    assert Category.objects.get(category_name=secao, category_store=lojaObject) != None

@given(u'o item "{item}" esta cadastrado no sistema com o preço "{preco}" na secao "{secao}" da loja "{loja}"')
def cadastrar_item(context,item,preco,secao,loja):
    views.create_new_item(None, item_name=item, qty= float(10), min_qty=float(0))
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

@when(u'eu tento cadastrar o preco "{preco}" do item "{item}" na secao "{secao}" da loja "{loja}"')
def tentar_cadastrar_preco(context,preco,item,secao,loja):
    itemObject = Item.objects.get(item_name=item)
    assert itemObject != None
    lojaObject = Store.objects.get(store_name=loja)
    secaoObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    assert secaoObject != None
    views.create_new_price(context, preco, secaoObject, itemObject)
    assert Price.objects.get(cost_product=preco, price_category=secaoObject, price_product=itemObject)

@then(u'o sistema sobrescreve o preco do item "{item}" na loja "{loja}" para o valor "{preco}"')
def sobrescrever_preco(context,item,loja,preco):
    itemObject = Item.objects.get(item_name=item)
    assert item != None
    lojaObject = Store.objects.get(store_name=loja)
    assert lojaObject != None
    #secaoObject = Category.objects.get(category_store=lojaObject)
    #assert  secaoObject != None
    priceObject = Price.objects.get(cost_product=preco, price_product=itemObject, price_category__category_store=lojaObject)
    assert priceObject != None
    assert (priceObject.cost_product) == float(preco)
    assert (priceObject.price_product == itemObject)
    assert (priceObject.price_category.category_store == lojaObject)

