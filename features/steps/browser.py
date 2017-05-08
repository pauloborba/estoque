from behave import given, when, then

@given('a user')
def step_impl(context):
    from django.contrib.auth.models import User
    u = User(username='foo', email='foo@example.com')
    u.set_password('bar')

@when('I log in')
def step_impl(context):
    br = context.browser
    br.open(context.browser_url('/account/login/'))
    br.select_form(nr=0)
    br.form['username'] = 'foo'
    br.form['password'] = 'bar'
    br.submit()

@then('I see my account summary')
def step_impl(context):
    br = context.browser
    response = br.response()
    assert response.code == 200
    assert br.geturl().endswith('/account/')

@then('I see a warm and welcoming message')
def step_impl(context):
    # Remember, context.parse_soup() parses the current response in
    # the mechanize browser.
    soup = context.parse_soup()
    msg = str(soup.findAll('h2', attrs={'class': 'welcome'})[0])
    assert "Welcome, foo!" in msg
