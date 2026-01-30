Feature: Sign In navigation

  Scenario: Logged out user can navigate to Sign In
    Given I open Target
    When I click the Account button
    And I click Sign In from the side navigation
    Then I should see the Sign In form
