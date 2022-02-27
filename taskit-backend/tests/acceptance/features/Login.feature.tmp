Feature: Login for user
  As a user, I would like to log in to the TaskIt System so that I can access my task list.

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
      | luke.skywalker@rebellion.com | jediknight457 |
      | scout@red.tf2.com            | EatASalad     |

  Scenario Outline: Successfully log in (normal flow)
    Given All users are logged out
    When The user attempts to log in with email address "<email>" and password "<password>"
    Then The user shall be logged in
    And The user shall see the task list for "<email>"

    Examples:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
      | luke.skywalker@rebellion.com | jediknight457 |

  Scenario Outline: Attempt to log in with invalid credentials (error flow)
    Given All users are logged out
    When The user attempts to log in with email address "<email>" and password "<password>"
    Then The user shall not be logged in
    And The error message "<error>" shall be displayed
    And The user shall be at the login page

    Examples:
      | email                  | password      | error                           |
      | obi-wan.kenobi@gar.gov |               | No password entered.            |
      | obi-wan.kenobi@gar.gov | jedimaster456 | Incorrect email address or password. |
      | scout@red.tf2.com      | ForceANature  | Incorrect email address or password. |
      |                        | rocketman7    | No username entered.            |
      | leia.organa@senate.gov | jediknight450 | Incorrect email address or password. |
      | spy@blue.tf2.com       | IAmTheSpy!    | Incorrect email address or password. |
