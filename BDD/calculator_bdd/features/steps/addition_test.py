from behave import *

@given(u'two valid integers')
def step_impl(context):
    print(u'STEP: Given two valid integers')


@when(u'adding the integers')
def step_impl(context):
    print(u'STEP: When adding the integers')
    context.result = _


@then(u'it should result to another integer')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it should result to another integer')