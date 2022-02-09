Feature: Sign up for user
  As a prospective user, I want to create an account with username and password
  so that I can log in later

  Background:
    Given The following users exist:
      | name             | username             | password      |
      | Obi-Wan Kenobi   | __obi-wan-kenobi__   | jedimaster123 |
      | Anakin Skywalker | __anakin-skywalker__ | jediknight456 |
      | Luke Skywalker   | __luke-skywalker__   | jediknight457 |

  Scenario Outline: Successfully create an account (normal flow)
    Given there is no existing username "<username>"
    When the user provides a new username "<username>" and a password "<password>"
    Then a new customer account shall be created
    Then the account shall have username "<username>" and password "<password>"

    Examples: 
      | name             | username             | password       |
      | Princess Lea     | __princess-lea__     | yourhighness57 |
      | Han Solo         | __Han-Solo__         | ladiesman70    |

  Scenario Outline: Create user with invalid parameters (error flow)
    When the user provides a new username "<username>" and a password "<password>"
    Then no new account shall be created
    Then an error message "<error>" shall be raised

    Examples: 
      | name             | username             | password       |error                         |
      | Princess Lea     | __princess-lea__     |                | No password entered          |
      | Princess Lea     | __princess-lea__     | NULL           | No password entered          |
      | Han Solo         | __Han-Solo__         | ladiesman70    |    
      | Boba Fett        | NULL                 | rocketman7     | No username entered          |
      | Boba Fett        |                      | rocketman7     | No username entered          |
      | Bob Skywalker    | __luke-Skywalker__   | jediknight450  | This username is taken       | 