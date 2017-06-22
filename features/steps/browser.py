import string
from behave import given, when, then

@given('a user')
def step_impl(context):
    from custom_user.models import customUser
    customUser.objects.create_superuser(username='test', email='foo@bar', password='test')

@when('I log in')
def step_impl(context):
    br = context.browser
    br.visit(context.base_url)
    br.fill("username", "test")
    br.fill("password", "test")
    button = br.find_by_tag('button')
    button.click()

@then('I am at the main page')
def step_impl(context):
    br = context.browser
    response = br.status_code
    assert response.code == 200
    assert br.url.endswith("/home/")
