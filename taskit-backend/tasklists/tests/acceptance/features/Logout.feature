Feature: Logout for user
  As a user, I would like to log out of the TaskIt system to ensure the security of my data.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |
      | Anakin Skywalker | __anakin-skywalker__ | jediknight456 |
      | Luke Skywalker   | __luke-skywalker__   | jediknight457 |

  Scenario Outline: Successfully log out (normal flow)
    Given "<username>" is logged in
    When "<username>" attempts to log out
    Then The user shall be logged out
    And The user shall be at the login page

    Examples:
      | username             |
      | __obi-wan-kenobi__   |
      | __anakin-skywalker__ |
      | __luke-skywalker__   |
