from behave import given, when, then
import optional

optional.init_opt_()

@given(u'The following users exist')
def step_impl(context):
    raise NotImplementedError('STEP: Given The following users exist')

@given(u'there is no existing username "{username}"')
def step_impl(context, username):
    raise NotImplementedError('STEP: Given there is no existing username "<username>"')

@when(u'the user provides a new username "{username:opt_?}" and a password "{password:opt_?}"')
def step_impl(context, username, password):
    raise NotImplementedError('STEP: When the user provides a new username "<username>" and a password "<password>"')

@then(u'a new customer account shall be created')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then a new customer account shall be created')

@then(u'the account shall have username "{username}" and password "{password}"')
def step_impl(context, username, password):
    raise NotImplementedError(u'STEP: Then the account shall have username "<username>" and password "<password>"')

@then(u'no new account shall be created')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then no new account shall be created')

@then(u'an error message "{error}" shall be raised')
def step_impl(context, error):
    raise NotImplementedError(u'STEP: Then an error message "<error>" shall be raised')
