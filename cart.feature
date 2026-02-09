Feature: Cart

  Scenario: “Your cart is empty” message is shown for empty cart
    Given I am on the Target home page
    When I open the cart
    Then I should see the empty cart message
