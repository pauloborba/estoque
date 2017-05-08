Feature: Demonstrate how to test Django with behave & mechanize

  Scenario: Logging in to our new Django site

    Given a user
    When I log in
    Then I am at the main page
