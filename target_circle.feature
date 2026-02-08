Feature: Target Circle page

  Scenario Outline: Verify Unlock added value story cards count
    Given I open the Target Circle page
    Then I should see "<expected_cards>" story cards under "Unlock added value"

    Examples:
      | expected_cards |
      | 2              |
