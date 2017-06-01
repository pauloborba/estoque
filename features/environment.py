from splinter import Browser
from selenium import webdriver
from sys import platform
import os

os_name = ''
if platform == "linux" or platform == "linux2":
    os_name = "linux"
elif platform == "darwin":
    os_name = "macos"
elif platform == "win32":
    os_name = "windows"
phantomjs_path = os.path.join(os.getcwd(),'features','driver',os_name,'phantomjs')
if os_name == "windows":
    phantomjs_path += ".exe"
executable_path = {'executable_path':phantomjs_path}


def remove_pdfs():
	files = os.listdir(os.getcwd())
	for file in files:
		if os.path.isfile(file) and file.startswith('lista'):
			os.remove(os.getcwd()+'/'+file)

def before_all(context):
	if os.path.isfile(os.getcwd()+'/lista.pdf'): #testa se há arquivo no diretório do processo
		os.remove(os.getcwd()+'/lista.pdf') #se houver, remova-o antes de começar os testes
	prof_settings =  {"browser.download.folderList": 2,\
			"browser.download.manager.showWhenStarting": False,\
			"browser.download.dir": os.getcwd(),\
			"browser.helperApps.neverAsk.saveToDisk": "application/pdf",\
			"pdfjs.disabled": True}
	context.browser = Browser('firefox', profile_preferences=prof_settings)
	#context.browser = Browser('phantomjs', **executable_path)

def after_all(context):
	remove_pdfs()
	context.browser.quit()
