from splinter import Browser
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

def before_all(context):
    #context.browser = Browser('firefox')
    context.browser = Browser('phantomjs', **executable_path)

def after_all(context):
    context.browser.quit()
