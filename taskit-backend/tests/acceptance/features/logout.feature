Feature: login for user
  As a user, I would like to login and logout of the TaskIt System to be able to easily access my account.

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |
      | Anakin Skywalker | __anakin-skywalker__ | jediknight456 |
      | Luke Skywalker   | __luke-skywalker__   | jediknight457 |

  Scenario: Successfully login to an account (normal flow)
    Given there is an existing username "<username>"
    When the user provides a new username "<username>" and a password "<password>"
    Then the user shall login to the account
    Examples: 
      | username             | password      |
      | __obi-wan-kenobi__   | jedimaster123 |
      | __anakin-skywalker__ | jediknight456 |
      | __luke-skywalker__   | jediknight457 |

  Scenario: login to an account with the incorrect parameter (error flow)
    When the user provides a new username "<username>" and a password "<password>"
    Then the user will remain on the login page
    Then an error message "<error>" shall be raised

    Examples: 
      | username             | password       |error                         |
      | __obi-wan-kenobi__   |                | No password entered          |
      | __obi-wan-kenobi__   | NULL           | No password entered          |
      | __obi-wan-kenobi__   | jedimaster456  | Incorrect password           |
      | __scout-from-tf2__   | ForceANature   | Incorrect password           |
      | NULL                 | rocketman7     | No username entered          |
      |                      | rocketman7     | No username entered          |
      | __leia-skywalker__   | jediknight450  | This username does not exist |
      | __spy-from-tf2__     | IAmTheSpy!     | This username does not exist | 