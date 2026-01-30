Feature: Empty cart

  Scenario: User can view an empty cart
    Given I open Target
    When I go to the cart
    Then I should see the cart is empty