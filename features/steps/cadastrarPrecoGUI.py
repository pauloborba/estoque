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
from splinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Testes GUI
before = []
after = []
driver = webdriver.Chrome()


#Cenario GUI 1

'''
@given(u'eu estou logado no sistema')
def logar(context):
    driver.get("http://localhost:8000/")
    user = driver.find_element_by_id("usernameInput")
    user.send_keys("admin")
    password = driver.find_element_by_id("pwdInput")
    password.send_keys("adminadmin")
    button = driver.find_element_by_id("buttonLogin")
    button.click()
    assert driver.current_url == "http://localhost:8000/home/"
'''

@given(u'o item "{item}" esta cadastrado no sistema')
def cadastrar_item_no_sistema(context, item):
    views.create_new_item(None, item_name=item, qty=10, min_qty=0)
    assert Item.objects.get(item_name=item) is not None


@given(u'a secao "{secao}" esta cadastrada para a loja "{loja}"')
def cadastrar_secao_loja(context, secao, loja):
    views.create_new_store(None, loja)
    lojaObject = Store.objects.get(store_name=loja)
    assert lojaObject is not None
    views.create_new_category(None, secao, lojaObject)
    categoriaObject = Category.objects.get(category_name=secao, category_store=lojaObject)
    assert categoriaObject is not None


@given(u'eu estou na pagina de cadastramento de precos')
def pagina_cadastrar_preco(context):
    driver.get("http://localhost:8000/home/")
    assert driver.current_url == "http://localhost:8000/home/"
    link = driver.find_element_by_id("criarPreco")
    link.click()
    assert driver.current_url == "http://localhost:8000/newPrice/"



@given(u'eu seleciono o item "{item}" na lista de itens cadastrados')
def item_esta_cadastrado(context, item):
    driver.find_element_by_class_name("select-dropdown").click()
    spans = driver.find_elements_by_tag_name("span")
    for s in spans:
        if (s.text == item):
            s.click()


@given(u'eu seleciono a secao "{secao}" da loja "{loja}" na lista de secoes')
def secao_esta_cadastrada(context, secao, loja):
    views.create_new_store(None, loja)
    store = Store.objects.get(store_name=loja)
    views.create_new_category(None, secao, store)
    category = Category.objects.get(category_name=secao, category_store=store)
    driver.find_element_by_class_name("select-dropdown2").click()
    spans = driver.find_elements_by_tag_name("span")
    for s in spans:
        if (s.text == category.category_store.store_name + " - " + category.category_name):
            s.click()


@given(u'eu preencho o campo preco com valor "{valor}"')
def campo_preenchido(context, valor):
    priceField = driver.find_element_by_id("priceInput")
    priceField.send_keys(valor)
    before = Price.objects.all()


@given(u'o item "{item}" na loja "{loja}" ainda nao possui um preco')
def preco_nao_cadastrado(context, item, loja):
    itemObject = Item.objects.get(item_name=item)
    lojaObject = Store.objects.get(store_name=loja)
    assert Price.objects.filter(price_product=itemObject, price_category__category_store=lojaObject).count() == 0


@when(u'eu tento cancelar o cadastramento do item "{item}" com o valor "{preco}" na loja "{loja}"')
def cancelar_cadastramento_preco(context, item, preco, loja):
    c = Price.objects.all().count()
    driver.find_element_by_id("cancelButton").click()


@then(u'eu estou na pagina de precos cadastrados')
def estou_pagina_precos_cadastrados(context):
    assert driver.current_url == "http://localhost:8000/priceList/"


@then(u'a lista de precos nao foi alterada')
def lista_nao_alterada(context):
    lista = driver.find_element_by_id("listaElementos")
    after = Price.objects.all()
    assert len(before) == len(after)

#Cenario GUI 2

@given(u'o campo de cadastramento de preco esta vazio')
def verifica_campo_vazio(context):
    campo = driver.find_element_by_id("priceInput")
    campo.send_keys(123)
    campo.clear()
    assert campo.text == ""

@when(u'eu tento cadastrar preco para o item "{item}" na loja "{loja}"')
def tentar_cadastrar_preco(context, item, loja):
    driver.find_element_by_tag_name("button").click()


@then(u'eu permaneco na pagina de cadastramento de precos')
def verifica_mesma_pagina(context):
    assert driver.current_url == "http://localhost:8000/newPrice/"

@then(u'eu vejo uma mensagem informando que falta inserir um preco')
def vejo_mensagem(context):
    pass
    #driver.find_element_by_class_name("toast")
    itens = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'toast')))
    assert (len(itens) > 0)
