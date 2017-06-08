import string
from behave import given, when, then
from django.test import Client, TestCase

@given('a user created')
def step_impl(context):
    from custom_user.models import customUser
    customUser.objects.create_superuser(username='test', email='foo@bar', password='test')

@when('I post to /')
def step_impl(context):
    c = Client()
    response = c.post('/', {'username': 'test', 'password': 'test'})
    context.response = response

@then('I recieve an 302 http status code')
def step_impl(context):
    assert 302 == context.response.status_code
