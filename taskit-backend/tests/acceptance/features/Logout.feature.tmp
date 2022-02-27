Feature: Logout for user
  As a user, I would like to log out of the TaskIt system to ensure the security of my data.

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
      | luke.skywalker@rebellion.com | jediknight457 |

  Scenario Outline: Successfully log out (normal flow)
    Given "<email>" is logged in
    When "<email>" attempts to log out
    Then The user shall be logged out
    And The user shall be at the login page

    Examples:
      | email                        |
      | obi-wan.kenobi@gar.gov       |
      | anakin.skywalker@gar.gov     |
      | luke.skywalker@rebellion.com |
