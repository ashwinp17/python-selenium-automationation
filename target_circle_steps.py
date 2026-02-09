from behave import given, then
from pages.target_circle_page import TargetCirclePage


@given("I open the Target Circle page")
def step_open_target_circle(context):
    context.page = TargetCirclePage(context.driver)
    context.page.open()


@then('I see {expected_count:d} storycards under "Unlock added value"')
def step_verify_storycards(context, expected_count):
    actual_count = context.page.unlock_added_value_tile_count()
    assert actual_count == expected_count, (
        f'Expected {expected_count} storycards under "Unlock added value", '
        f"but found {actual_count}"
    )
