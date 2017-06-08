Feature: Demonstrate controller test

  Scenario: Logging in to our new Django site

    Given a user created
    When I post to /
    Then I recieve an 302 http status code
