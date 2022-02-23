Feature: Sign up for user
  As a prospective user, I want to create an account with email and password
  so that I can log in later

  Background:
    Given The following users exist:
      | email                  | password       |
      | luke.skywalker@rebellion.com | jediknight457 |

  Scenario Outline: Successfully create an account (normal flow)
    Given there is no existing account with email address "<email>"
    When the user provides a new email address "<email>" and a password "<password>"
    Then a new customer account shall be created
    Then the account shall have email address "<email>" and password "<password>"

    Examples:
      | email                  | password       |
      | leia.organa@senate.gov | yourhighness57 |
      | han.solo@army.gov      | ladiesman70    |

  Scenario Outline: Create user with invalid parameters (error flow)
    When the user provides a new email address "<email>" and a password "<password>"
    Then no new account shall be created
    Then there will exist no user with email address "<email>" and a password "<password>"
    Then an error message "<error>" shall be raised

    Examples:
      | email                        | password      | error                                 |
      | leia.organa@senate.gov       |               | No password entered.                  |
      |                              | rocketman7    | No email address entered.             |

  Scenario Outline: Create user using an email that is already taken (error flow)
    When the user provides a new email address "<email>" and a password "<password>"
    Then no new account shall be created
    Then there will exist a user with email address "<email>" and a password "<password>"
    Then an error message "<error>" shall be raised

    Examples:
      | email                        | password      | error                                 |
      | luke.skywalker@rebellion.com | jediknight450 | This email address is already in use. |

  Scenario Outline: Create user using invalid email (error flow)
    When the user provides a new email address "<email>" and a password "<password>"
    Then no new account shall be created
    Then there will exist no user with email address "<email>" and a password "<password>"
    Then an error message "<error>" shall be raised

    Examples:
      | email              | password      | error         |
      | blablablablablabla | jediknight450 | Invalid email |
