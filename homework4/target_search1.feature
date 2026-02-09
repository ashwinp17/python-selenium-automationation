Feature: Target product search

  Scenario Outline: User can search for a product on Target
    Given I open "<url>"
    When I search for "<query>"
    Then I see search results for "<query>"

    Examples:
      | url                  | query |
      | https://www.target.com | tea   |
      | https://www.target.com | coffee|
