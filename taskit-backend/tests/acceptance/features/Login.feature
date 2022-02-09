Feature: Login for user
  As a user, I would like to log in to the TaskIt System so that I can access my task list.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |
      | Anakin Skywalker | __anakin-skywalker__ | jediknight456 |
      | Luke Skywalker   | __luke-skywalker__   | jediknight457 |
	  | Scout            | __scout-from-tf2__   | EatASalad     |

  Scenario Outline: Successfully log in (normal flow)
    Given All users are logged out
    When The user attempts to log in with username "<username>" and password "<password>"
    Then The user shall be logged in
    And The user shall see the task list for "<username>"

    Examples:
      | username             | password      |
      | __obi-wan-kenobi__   | jedimaster123 |
      | __anakin-skywalker__ | jediknight456 |
	  | __luke-skywalker__   | jediknight457 |

  Scenario Outline: Attempt to log in with invalid credentials (error flow)
    Given All users are logged out
    When The user attempts to log in with username "<username>" and password "<password>"
    Then The user shall not be logged in
    And The error message "<error>" shall be displayed
    And The user shall be at the login page

    Examples:
      | username             | password       | error                           |
      | __obi-wan-kenobi__   |                | No password entered.            |
      | __obi-wan-kenobi__   | NULL           | No password entered.            |
      | __obi-wan-kenobi__   | jedimaster456  | Incorrect username or password. |
      | __scout-from-tf2__   | ForceANature   | Incorrect username or password. |
      | NULL                 | rocketman7     | No username entered.            |
      |                      | rocketman7     | No username entered.            |
      | __leia-skywalker__   | jediknight450  | Incorrect username or password. |
      | __spy-from-tf2__     | IAmTheSpy!     | Incorrect username or password. |
