from splinter import Browser

executable_path = {'executable_path':'./features/driver/linux/phantomjs'}

def before_all(context):
    context.browser = Browser('phantomjs', **executable_path)

def after_all(context):
    context.browser.quit()
