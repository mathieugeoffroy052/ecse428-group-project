Feature: Organize Tasks
  As a user, I wish to create a task list.

  Background:
    Given The following users exist:
      | email                        | password      |
      | obi-wan.kenobi@gar.gov       | jedimaster123 |
      | anakin.skywalker@gar.gov     | jediknight456 |
      | luke.skywalker@rebellion.com | jediknight457 |

    Given The following lists exist:
      | list_name                        | owner                        |
      | Achieve victory in the monarchy  | obi-wan.kenobi@gar.gov       |
      | Obliterate the tomato metropolis | luke.skywalker@rebellion.com |

  Scenario Outline: Successfully add task list (normal flow)
    Given "<email>" is logged in
    When The user "<email>" attempts to create the task list "<name>"
    Then the task list "<name>" shall exist in the system
    Then "<email>" shall have a task list called "<name>"
    Then the number of task lists in the system shall be "3"
    And The message "Task list created succesfully." shall be displayed

    Examples:
      | email                        | name                            |
      | obi-wan.kenobi@gar.gov       | Accompany ally to the wet swamp |
      | anakin.skywalker@gar.gov     | Heal injured ally               |
      | luke.skywalker@rebellion.com | Drink carafe rapidly            |
      | luke.skywalker@rebellion.com | Achieve victory in the monarchy |

  Scenario Outline: Create a task list with invalid parameters (error flow)
    Given "<email>" is logged in
    When the user "<email>" attempts to create the task list "<name>"
    Then the number of task lists in the system shall be "2"
    Then shall not be a list called "<name>"
    Then no new task list shall be created
    Then The error message "<error>" shall be displayed

    Examples:
      | email                    | name | error                        |
      | obi-wan.kenobi@gar.gov   | NULL | This field may not be blank. |
      | anakin.skywalker@gar.gov |      | This field may not be blank. |

  Scenario: Create a task list with duplicate name (error flow)
    Given "luke.skywalker@rebellion.com" is logged in
    When the user "luke.skywalker@rebellion.com" attempts to create the task list "Obliterate the tomato metropolis"
    Then the number of task lists in the system shall be "2"
    Then the task list "Obliterate the tomato metropolis" shall exist in the system
    Then no new task list shall be created
    Then The error message "This list name already exists." shall be displayed

  Scenario Outline: Attempt to create task list without being logged in (error flow)
    Given All users are logged out
    When The user attempts to create the task list of "<email>" called "<name>"
    Then the number of task lists in the system shall be "2"
    Then shall not be a list called "<name>"
    Then no new task list shall be created
    Then The error message "Authentication credentials were not provided." shall be displayed

    Examples:
      | email                  | name                   |
      | obi-wan.kenobi@gar.gov | Spend virtual currency |
