Feature: Target - Product Search

  @search
  Scenario Outline: User can search for a product on Target
    Given I open "<base_url>"
    When I search for "<search_term>"
    Then search results for "<search_term>" are shown

    Examples:
      | base_url                | search_term |
      | https://www.target.com/ | tea         |
      | https://www.target.com/ | coffee      |

  @circle
  Scenario: Target Circle page has 2 storycards under "Unlock added value"
    Given I open "https://www.target.com/circle"
    Then I see 2 storycards under "Unlock added value"

