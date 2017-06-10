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
import time

# Testes GUI
before = []
after = []
#driver = webdriver.Chrome()


def getPort(url): #Retorna a porta da URL
    return url.split(':')[2].split('/')[0]

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
    context.browser.visit(context.base_url+'/home')
    assert context.browser.url == (context.base_url+'/home/')
    link = context.browser.find_by_id('criarPreco')
    link.click()
    assert context.browser.url == (context.base_url+'/newPrice/')


@given(u'eu estou na pagina principal')
def pagina_principal(context):
    context.browser.visit(context.base_url+'/home')
    assert context.browser.url == (context.base_url+'/home/')

@when(u'eu seleciono a opcao de ver historico')
def ver_historico(context):
    link = context.browser.find_by_id('history')
    link.click()

@when(u'eu seleciono o item "{item}" na lista de itens cadastrados')
def item_esta_cadastrado(context, item):
    dropdown = context.browser.find_by_xpath("//select[@id='itemInput']")
    for option in dropdown.find_by_tag('option'):
        if option.text == item:
            option.click()
            break



@when(u'eu seleciono a secao "{secao}" da loja "{loja}" na lista de secoes')
def secao_esta_cadastrada(context, secao, loja):
    views.create_new_store(None, loja)
    store = Store.objects.get(store_name=loja)
    views.create_new_category(None, secao, store)
    category = Category.objects.get(category_name=secao, category_store=store)
    dropdown = context.browser.find_by_xpath("//select[@id='itemInput']")
    for option in dropdown.find_by_tag('option'):
        if option.text == category.category_store.store_name + " - " + category.category_name:
            option.click()
            break


@given(u'o item "{item}" na loja "{loja}" ainda nao possui um preco')
def preco_nao_cadastrado(context, item, loja):
    itemObject = Item.objects.get(item_name=item)
    lojaObject = Store.objects.get(store_name=loja)
    assert Price.objects.filter(price_product=itemObject, price_category__category_store=lojaObject).count() == 0


@when(u'eu preencho o campo preco com valor "{valor}"')
def campo_preenchido(context, valor):
    priceField = context.browser.find_by_id('priceInput')
    priceField.fill(valor)
    before = Price.objects.all()


@when(u'eu tento cancelar o cadastramento do item "{item}" com o valor "{preco}" na loja "{loja}"')
def cancelar_cadastramento_preco(context, item, preco, loja):
    context.browser.find_by_id('cancelButton').click()


@then(u'eu estou na pagina de precos cadastrados')
def estou_pagina_precos_cadastrados(context):
    assert context.browser.url == (context.base_url+'/priceList/')


@then(u'a lista de precos nao foi alterada')
def lista_nao_alterada(context):
    lista = context.browser.find_by_id('listaElementos')
    after = Price.objects.all()
    assert len(before) == len(after)

#Cenario GUI 2

@given(u'o campo de cadastramento de preco esta vazio')
def verifica_campo_vazio(context):
    campo = context.browser.find_by_id('priceInput')
    campo.fill(123)
    campo.fill("")
    assert campo.text == ""


@when(u'eu tento cadastrar preco para o item "{item}" na loja "{loja}"')
def tentar_cadastrar_preco(context, item, loja):
    context.browser.find_by_tag('button').click()


@then(u'eu permaneco na pagina de cadastramento de precos')
def verifica_mesma_pagina(context):
    assert context.browser.url == (context.base_url+'/newPrice/')


@then(u'eu vejo uma mensagem informando que falta inserir um preco')
def vejo_mensagem(context):
    itens = WebDriverWait(context.browser.driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'toast')))
    assert (len(itens) > 0)


@then(u'eu estou na pagina de historicos')
def pagina_historico(context):
    assert context.browser.url == (context.base_url + '/priceHistory/')


@then(u'eu vejo o produto "{item}" no historico de precos')
def vejo_item_historico(context, item):
    assert context.browser.is_text_present(item)

