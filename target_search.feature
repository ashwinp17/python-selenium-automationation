Feature: Target product search

  Scenario Outline: User can search for a product on Target
    Given I open the Target home page
    When I search for "<search_term>"
    Then search results for "<search_term>" are shown

    Examples:
      | search_term |
      | tea         |
      | coffee      |

