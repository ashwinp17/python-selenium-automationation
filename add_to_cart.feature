Feature: Add a product to cart

  Scenario: User can add a product to cart and see it in the cart
    Given I open Target home page
    When I search for "tea"
    And I open the first product result
    And I add the product to the cart
    Then I should see at least 1 item in the cart
