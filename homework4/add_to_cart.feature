Feature: Add product to cart

  Scenario: Add any Target product to the cart and verify it is there
    Given I open Target home page
    When I search for "tea"
    And I open the first product result
    And I add the product to the cart
    Then I open the cart
    And the cart is not empty

