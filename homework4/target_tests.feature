Feature: Product Search on Target

  @search
  Scenario Outline: User can search for a product on Target
    Given I open the Target home page
    When I search for "<product>"
    Then I should see search results related to "<expected_keyword>"

    Examples:
      | product              | expected_keyword |
      | tea                  | tea              |
      | coffee               | coffee           |
      | paper towels         | paper            |

